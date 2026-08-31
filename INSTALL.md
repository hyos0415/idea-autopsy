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
- **훅/스킬을 고쳤는데 반영이 안 됨** → 설치본은 `plugin.json`의 `version` 문자열로 캐시되는
  **복사본**입니다 (`~/.claude/plugins/cache/<마켓>/<플러그인>/<버전>/`). 버전을 올리지 않으면
  `claude plugin update`가 "already at the latest version"이라며 옛 복사본을 유지합니다(실측).
  개발 중에는 `claude --plugin-dir ./plugin`(항상 라이브)을 쓰고, 배포할 때 버전을 올리세요.
- **훅이 도는 것 같은데 아무 일도 없음 (특히 Windows)** → 셔뱅의 `python3`가 Microsoft Store
  앱 실행 별칭 스텁일 수 있습니다. 스텁은 exit 0으로 끝나 정상 통과처럼 보입니다.
  `python3 -c "print(42)"`가 42를 내놓는지 확인하세요. rigor는 `hooks/run-rigor.sh` 런처가
  `python3 → python → py` 중 실제로 동작하는 것을 골라 이 문제를 우회합니다.
  훅이 실제로 돌았는지는 `RIGOR_LOG=<파일>` 환경변수로 확인하세요 — 한 줄도 없으면 미실행입니다.
- **마켓플레이스 인식 실패** → 레포 루트 `.claude-plugin/marketplace.json` 존재 확인
- **뭐가 잘못됐는지 모르겠음** → `claude --debug` 로 로딩 로그 확인
- **훅 반송문이 무시됨** → Stop 훅에서 `hookSpecificOutput.decision`은 차단되지 않습니다.
  최상위 `{"decision":"block","reason":"..."}` 를 쓰세요 (실측, hooks/rigor-spec.md 참조)
