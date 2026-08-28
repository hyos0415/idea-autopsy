# 설치 가이드 (INSTALL.md)

> 세 가지 경로가 있습니다. 대부분의 사용자는 **A**면 충분합니다.
> (검증 기준: Claude Code 공식 plugins-reference, 2026-08 확인)

## A. 채팅에서 쓰기 (claude.ai / 데스크탑 앱) — 비개발자 포함 누구나

설치라고 할 것도 없습니다. 둘 중 하나:

1. **스킬 등록**: 설정의 스킬(기능) 메뉴에서 `skills/coroner/SKILL.md` 내용을 스킬로 저장.
   executor, design-coroner도 각각 등록. 이후 "이 아이디어 만들 가치 있어?"라고 물으면 자동 발동
2. **붙여넣기 (등록조차 귀찮다면)**: 새 대화 첫 메시지에 `SKILL.md` 전문 + 빈 줄 + 아이디어 한 문장

## B. Claude Code에서 쓰기 (개발자, 내 컴퓨터에만)

**B-1. 스킬로만 (가장 간단, 권장 시작점)** — 마켓플레이스·설치 명령 불필요:

```bash
# 레포를 클론했다면:
cp -r skills/coroner skills/executor skills/design-coroner ~/.claude/skills/
# 다음 세션부터 자동 인식. 끝.
```

**B-2. 플러그인째 로컬 로드** (rigor 훅 개발·테스트용, 세션 한정):

```bash
claude --plugin-dir ./plugin
# 확인: 세션에서 /plugin → Errors 탭이 비어 있어야 정상
```

## C. 마켓플레이스로 설치 (다른 사람이 한 줄로 설치하게)

이 레포 루트에 `.claude-plugin/marketplace.json`이 있어야 합니다 (동봉됨 — 없으면
`marketplace add`가 레포를 인식하지 못합니다. 흔한 함정).

사용자 쪽 설치:

```bash
claude plugin marketplace add hyos0415/idea-autopsy
claude plugin install idea-autopsy@idea-autopsy
# "Run /reload-plugins to activate." 가 뜨면 그대로 실행
```

## 배포 전 검증 (레포 주인용 체크리스트)

로컬에서 이 두 명령이 통과해야 푸시합니다 — 이 검시소의 규율상, 검증 없는 배포는 없습니다:

```bash
claude plugin validate ./plugin          # 매니페스트·스킬 frontmatter 스키마 검사
claude --plugin-dir ./plugin             # 실제 로드 → /plugin Errors 탭 확인, 스킬 발동 1회 테스트
```

## 자주 걸리는 곳 (공식 문서의 함정 목록에서)

- **스킬이 안 보임** → `skills/`가 플러그인 루트에 있어야 함 (`.claude-plugin/` 안에 넣으면 무시됨)
- **훅이 안 돎** → 스크립트 실행 권한 (`chmod +x`), 이벤트명 대소문자 (`PostToolUse`)
- **마켓플레이스 인식 실패** → 레포 루트 `.claude-plugin/marketplace.json` 존재 확인
- **뭐가 잘못됐는지 모르겠음** → `claude --debug` 로 로딩 로그 확인
- rigor 훅은 현재 **사양만 존재** (hooks/rigor-spec.md) — hooks.json이 없으므로 아무 훅도
  로드되지 않는 것이 정상입니다
