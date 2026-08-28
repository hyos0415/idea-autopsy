#!/usr/bin/env python3
"""rigor — 주장-로그 대조 게이트 (Stop 훅)

산출물이 주장하는 근거([WEB]/[FILE] 태그, "확인했다/검증했다")에 대응하는
실제 도구 호출이 이번 세션 로그에 있는지 대조한다. 없으면 차단하고 반송한다.

잡는 것은 "적게 한 것"이 아니라 "안 했는데 했다고 한 것"이다.
탐색을 줄였다고 정직하게 쓴 산출물은 통과 대상이다.

주장은 last_assistant_message에서 읽는다 — transcript_path는 lag가 있어
마지막 응답이 아직 기록되지 않은 상태로 읽힌다. 실행 기록만 transcript에서 읽는다.

stop_hook_active는 입력에 존재하지만 쓰지 않는다 — 반송 후 턴에서도 재위조는
잡아야 하고, 반복 제한은 CLAUDE_PLUGIN_DATA의 세션별 카운터가 담당한다.
"""

import json
import os
import re
import sys

MAX_RETURNS = 2

# 태그 → 그 태그를 정당화하는 도구
TAG_TOOLS = {
    "WEB": {"WebSearch", "WebFetch"},
    "FILE": {"Read", "Glob", "Grep", "Bash", "NotebookEdit"},
}

# 도구 호출 없이 쓰면 위조가 되는 검증 주장
VERIFY_PATTERNS = [
    r"확인했",
    r"확인함",
    r"검증했",
    r"직접 확인",
    r"문서를? 확인",
    r"README를? 확인",
    r"원문을? 확인",
    r"검색해서 확인",
    r"web[_ ]?fetch",
]
VERIFY_TOOLS = {"WebSearch", "WebFetch", "Read", "Glob", "Grep", "Bash"}

# 이 게이트가 감시하는 산출물인지 판별 — 아니면 그냥 통과시킨다
ARTIFACT_MARKERS = [
    r"\[(?:WEB|FILE|INPUT|SKILL|MEMORY|INFERENCE)\]",
    r"Build Recommendation",
    r"Just Use AI",
    r"Configure Existing Tools",
    r"capability 분해",
    r"failure log",
    r"Adopt/Adapt/Create",
]


def fail_open(msg):
    """훅 자신의 오류로 사용자를 막지 않는다."""
    print(f"rigor: {msg}", file=sys.stderr)
    sys.exit(0)


def load_input():
    try:
        return json.load(sys.stdin)
    except Exception as exc:  # noqa: BLE001
        fail_open(f"입력 파싱 실패 — {exc}")


def tools_used(transcript_path):
    """세션 전체의 tool_use 이름 집합. 턴 단위로 좁히지 않는 것은 의도적이다 —
    coroner 한 판정이 여러 턴에 걸치므로, 좁히면 오탐이 난다."""
    used = set()
    if not transcript_path or not os.path.exists(transcript_path):
        return None
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                content = (entry.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block.get("name")
                        if name:
                            used.add(name.split("__")[-1])
    except OSError as exc:
        print(f"rigor: transcript 읽기 실패 — {exc}", file=sys.stderr)
        return None
    return used


def sentences(text):
    parts = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts.extend(s.strip() for s in re.split(r"(?<=[.!?。])\s+", line) if s.strip())
    return parts


def find_violations(message, used):
    """대응 호출이 없는 주장만 모은다."""
    violations = []
    for sentence in sentences(message):
        for tag, needed in TAG_TOOLS.items():
            if f"[{tag}]" in sentence and not (needed & used):
                violations.append((f"[{tag}] 태그", sentence))
                break
        else:
            if not (VERIFY_TOOLS & used) and any(
                re.search(p, sentence, re.IGNORECASE) for p in VERIFY_PATTERNS
            ):
                violations.append(("검증 주장", sentence))
    return violations


def counter_path(session_id):
    root = os.environ.get("CLAUDE_PLUGIN_DATA")
    if not root:
        return None
    directory = os.path.join(root, "rigor")
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        return None
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", session_id or "unknown")
    return os.path.join(directory, f"{safe}.json")


def read_count(path):
    if not path or not os.path.exists(path):
        return 0
    try:
        with open(path, encoding="utf-8") as fh:
            return int(json.load(fh).get("returns", 0))
    except (OSError, ValueError, TypeError):
        return 0


def write_count(path, count):
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"returns": count}, fh)
    except OSError:
        pass


def main():
    data = load_input()
    message = data.get("last_assistant_message") or ""
    if not message.strip():
        sys.exit(0)

    # 감시 대상 산출물이 아니면 통과
    if not any(re.search(m, message, re.IGNORECASE) for m in ARTIFACT_MARKERS):
        sys.exit(0)

    used = tools_used(data.get("transcript_path"))
    if used is None:
        fail_open("transcript를 읽을 수 없어 대조를 생략함")

    violations = find_violations(message, used)
    if not violations:
        sys.exit(0)

    path = counter_path(data.get("session_id"))
    count = read_count(path)

    if count >= MAX_RETURNS:
        # 정교화된 위조를 무한 반송하지 않는다 — 플래그만 남기고 통과시킨다
        print(
            json.dumps(
                {
                    "systemMessage": (
                        f"rigor: 교정 불가 — {MAX_RETURNS}회 반송 후에도 "
                        f"근거 없는 주장 {len(violations)}건이 남아 있습니다. "
                        "산출물을 신뢰하지 마십시오."
                    )
                },
                ensure_ascii=False,
            )
        )
        sys.exit(0)

    write_count(path, count + 1)

    listed = "\n".join(f"- ({kind}) {text}" for kind, text in violations[:5])
    more = f"\n외 {len(violations) - 5}건" if len(violations) > 5 else ""
    reason = (
        "rigor 게이트(이 플러그인의 Stop 훅)가 방금 작성한 산출물을 세션의 도구 호출 "
        "기록과 대조했습니다. 다음 주장에는 대응하는 실행 기록이 없습니다:\n"
        f"{listed}{more}\n\n"
        "둘 중 하나로 해소하세요 — (1) 해당 도구를 실제로 실행해 근거를 확보하고 그 "
        "부분만 고쳐 다시 제출, 또는 (2) 탐색을 줄이기로 했다면 태그를 [INFERENCE]/"
        "[MEMORY]로 바꾸고 확인하지 않았다는 사실을 명시. 탐색을 줄인 것 자체는 위반이 "
        "아니며, 하지 않은 확인을 했다고 쓰는 것만 위반입니다."
    )

    # 최상위 decision/reason 이어야 한다. 공식 문서의 hookSpecificOutput 예시는
    # Stop에서 차단되지 않는 것을 실측으로 확인했다(2026-08). exit 2 + stderr도
    # 차단은 되지만, 반송문이 프롬프트 인젝션으로 읽혀 모델이 거부한다.
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
