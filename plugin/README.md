# idea-autopsy plugin — EXPERIMENTAL / 미검증

이 디렉토리는 스킬 3종을 Claude Code 플러그인으로 묶은 스캐폴드입니다.
**설치·동작 검증을 아직 거치지 않았습니다** — 이 검시소의 규율상 검증 없는 "작동" 주장은 금지이므로,
아래 체크리스트를 통과하기 전에는 실험 단계로 취급하세요.

- [x] `claude --plugin-dir ./plugin` 로 로컬 로드, 스킬 3종 트리거 확인
- [x] `/plugin` Errors 탭에 오류 없음 확인
- [x] rigor 훅 구현 + 자체 검증 체크리스트 통과 (hooks/rigor-spec.md 하단 참조)
- [x] 마켓플레이스 등록 (`hyos0415/idea-autopsy`)
- [ ] 스킬 3종의 판정 품질 실런 검증 — 미완. 이것이 EXPERIMENTAL의 실제 사유

rigor는 **구현되어 동작합니다** (hooks/hooks.json + hooks/rigor.py). 근거: Δ 실험 —
지침은 위조되므로 강제는 코드(훅)여야 함. 구현 중 실측한 API 사실은 hooks/rigor-spec.md에.
