#!/bin/sh
# rigor 런처 — 실제로 동작하는 파이썬 인터프리터를 골라 rigor.py에 stdin을 넘긴다.
#
# 왜 필요한가 (실측 2026-08-31, Windows 11):
# hooks.json이 rigor.py를 직접 실행하면 셔뱅의 `python3`가 Microsoft Store
# 앱 실행 별칭 스텁으로 잡힌다. 이 스텁은 "Python was not found"를 출력하고
# **exit 0**으로 끝나므로, Claude Code는 훅이 정상 통과했다고 판단한다.
# 결과적으로 Windows에서는 게이트가 한 번도 돌지 않은 채 조용히 통과시킨다 —
# fail-open보다 나쁘다. 로그조차 남지 않아 훅이 돌고 있다는 착각을 남긴다.
#
# 그래서 이름이 아니라 **동작**으로 인터프리터를 고른다: print(42)가 실제로
# 42를 내놓는 것만 인정한다. 스텁은 이 검사를 통과하지 못한다.
RIGOR="$(dirname "$0")/rigor.py"

for p in python3 python py; do
  command -v "$p" >/dev/null 2>&1 || continue
  [ "$("$p" -c "print(42)" 2>/dev/null)" = "42" ] || continue
  exec "$p" "$RIGOR"
done

# 쓸 수 있는 파이썬이 없으면 fail-open — 훅 자신의 부재로 사용자를 막지 않는다.
echo "rigor: 실행 가능한 python을 찾지 못해 대조를 생략함" >&2
exit 0
