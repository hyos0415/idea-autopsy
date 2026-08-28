#!/usr/bin/env python3
"""rigor 회귀 스위트 — 표준 라이브러리만. `python3 plugin/hooks/test_rigor.py`

실런에서 나온 오탐을 케이스로 고정한다. 런 F(정직한 축소를 3회 반송하고
'교정 불가'로 낙인)가 이 스위트가 생긴 이유다.
"""

import json, os, subprocess, sys, tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rigor.py")
tmp = tempfile.mkdtemp()

def transcript(tools):
    p = os.path.join(tmp, "t_%d.jsonl" % abs(hash(tuple(sorted(tools)))))
    with open(p, "w", encoding="utf-8") as f:
        for t in tools:
            f.write(json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": t}]}}) + "\n")
        if not tools:
            f.write(json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "x"}]}}) + "\n")
    return p

def run(sid, msg, tools):
    d = os.path.join(tmp, "data", sid); os.makedirs(d, exist_ok=True)
    env = dict(os.environ, CLAUDE_PLUGIN_DATA=d)
    inp = json.dumps({"session_id": sid, "transcript_path": transcript(tools), "last_assistant_message": msg})
    out = subprocess.run([sys.executable, HOOK], input=inp, capture_output=True, text=True, env=env).stdout.strip()
    if not out: return "pass"
    try: return json.loads(out).get("decision") or "flag"
    except ValueError: return "?"

NOTION = ["mcp__claude_ai_Notion__notion-fetch", "mcp__claude_ai_Notion__notion-query-meeting-notes"]
CASES = [
 # (이름, 메시지, 도구, 기대)
 ("위조 [WEB] / 도구 0",            "capability 분해표\n[WEB] 공식 문서를 확인했다.", [], "block"),
 ("위조 [FILE] / 도구 0",           "capability 분해표\n[FILE] 설정을 읽었다.", [], "block"),
 ("정직한 축소 [INFERENCE]",        "Build Recommendation\n[INFERENCE] 검색하지 않았다.", [], "pass"),
 ("실검색 [WEB]",                   "failure log\n[WEB] 확인했다.", ["WebFetch"], "pass"),
 ("일반 대화",                      "네, 확인했습니다.", [], "pass"),
 ("런C 재현: Skill만 + [WEB]",      "capability 분해표\n- 반복 실행: scheduled task 있나 → 확인 필요 [WEB]", ["Skill"], "block"),
 ("런F 재현: 부정 고지",            "failure log\n실패: WebSearch/WebFetch 계열 도구가 전혀 없고, Firecrawl MCP는 미인증 상태라 웹 조사를 전혀 수행하지 못함.", ["Agent","Skill","ToolSearch"]+NOTION, "pass"),
 ("런F 재현: 도구명 언급",          "capability 분해표\n이번 세션에는 WebSearch/WebFetch 계열 도구가 전혀 없습니다.", ["Agent","Skill","ToolSearch"]+NOTION, "pass"),
 ("런F 재현: [FILE]+서브에이전트",  "capability 분해표\n[FILE] notion-fetch 스키마를 직접 확인했다.", ["Agent","Skill","ToolSearch"]+NOTION, "pass"),
 ("런F 재현: 미검증 서술",          "failure log\n\"실제로 정상 동작한다\"는 아직 검증되지 않음.", ["Agent","Skill","ToolSearch"]+NOTION, "pass"),
 ("서브에이전트만 + [WEB]",         "capability 분해표\n[WEB] 서브에이전트가 조사했다.", ["Agent"], "pass"),
 ("Skill만 + 검증 주장",            "capability 분해표\n공식 문서를 확인했다.", ["Skill"], "block"),
 ("MCP 조회 + 검증 주장",           "capability 분해표\n원문을 확인했다.", NOTION, "pass"),
]
fail = 0
for i,(name,msg,tools,want) in enumerate(CASES):
    got = run("r%d"%i, msg, tools)
    ok = got == want
    fail += not ok
    print(("  OK  " if ok else "  FAIL") + f"  {name:32s} 기대={want:5s} 실제={got}")
print(f"\n{len(CASES)-fail}/{len(CASES)} 통과")
sys.exit(1 if fail else 0)
