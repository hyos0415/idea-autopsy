# build-or-use 스킬 검증 절차

이 스킬은 그 자체가 검증 대상 프로토타입이다. 향후 공모전 프로젝트의 baseline이 될 수 있으므로, 처음부터 웹서비스·백엔드·Vector DB·Agent framework를 만들지 않는다. **Skill만으로 충분하다면 "별도 제품을 만들 필요가 없다"는 결론도 받아들인다.** 반대로 반복적인 실패가 관찰되면 그 실패가 향후 제품 요구사항이 된다.

## 실행 규칙

- 각 케이스를 스킬 workflow대로 실제로 수행한다 (분해 → 탐색 → 검증 → 판정 → failure log).
- **"예상 비교 기준"과 "관찰할 것"은 채점자용이다. 판정 과정에 미리 노출하거나 그 방향으로 결론을 유도하지 않는다.**
- 사람의 사후 판단은 테스트 이후 사용자가 작성한다. 스킬에게 정답으로 미리 제공하지 않는다.

## Case 1 — AI 학습 복습 시스템

입력:
> "내가 공부한 CS 개념 중 부족한 부분을 매일 조금씩 물어보고 틀린 부분을 다시 설명해주는 서비스를 만들고 싶다."

관찰할 것: GPT/Claude 자체 기능, 예약 작업, conversation state, memory, ontology system 필요 여부
예상 비교 기준: 기존 AI 기능만으로 상당 부분 해결 가능할 가능성이 높다.

## Case 2 — 사진 선별

입력:
> "사진을 많이 찍는데 비슷한 사진을 한꺼번에 묶어보고 그중 좋은 사진 하나만 남기고 싶다."

관찰할 것: 기존 사진 관리 서비스, Immich 같은 self-hosted solution, similarity grouping, 큰 화면 비교, 별도 AI ranking 필요 여부, local/private processing 가능 여부
예상 비교 기준: 기존 도구를 먼저 쓰고, 남는 선별 병목만 custom 개발 후보가 될 가능성이 높다.

## Case 3 — AI 대화 → 블로그

입력:
> "AI랑 이야기하다가 나온 괜찮은 아이디어와 생각을 모아두고 나중에 블로그 초안으로 만들고 싶다."

관찰할 것: Obsidian / Markdown / knowledge management, 기존 Skill, conversation export, blog drafting workflow, 별도 제품 가치
예상 비교 기준: Skill 또는 workflow 수준으로 충분할 가능성이 높다.

## Case 4 — 금융상품 실제 금리 계산

입력:
> "예금·적금 상품을 비교할 때 광고 최고금리 말고 내가 실제로 받을 수 있는 금리를 알고 싶다."

관찰할 것: 범용 LLM만으로 가능한 부분, 외부 금융 데이터 필요성, structured condition schema, deterministic calculation, HITL, 검증 가능성, 별도 시스템 필요 여부
예상 비교 기준: Custom Product가 살아남을 가능성이 높은 비교군이다. 단, 이 예상 답을 판정 과정에 노출해 맞추게 하지 않는다.

## Case 5 — 개인 기록 플랫폼

입력:
> "사진이나 글을 SNS에 올리기보다 내가 했던 요리, 카페, 옷, 생각 같은 걸 예쁘게 개인 기록으로 남기고 싶다."

관찰할 것: Notion, Obsidian, journaling service, 기존 개인 기록 앱, 범용 AI와 기존 제품 조합, custom UX가 제공하는 가치

## Self-Test (가장 중요)

이 스킬에게 자기 자신을 평가시킨다.

입력:
> "사용자가 만들고 싶은 AI 서비스 아이디어를 입력하면, 기존 GPT/Claude 기능과 Skill, Plugin, MCP, 오픈소스 도구를 찾아보고 새로 개발할 필요가 있는지 판단해주는 서비스를 만들고 싶다."

관찰할 것:
- 자기 자신을 Skill로 충분하다고 판단하는가
- 어떤 기능 때문에 별도 제품이 필요하다고 판단하는가
- 검색 범위의 한계를 발견하는가
- semantic retrieval 문제를 발견하는가
- 실제 실행/eval 부재를 문제로 보는가
- 근거 없이 웹서비스 개발을 추천하는가
- multi-source retrieval 필요성을 발견하는가
- capability verification 필요성을 발견하는가

## 결과 기록

각 케이스마다 남길 것:
- 스킬의 최종 결론
- 사람이 아는 현실과 비교했을 때 맞는지
- 놓친 기존 기능/제품
- Search Failure / Capability Failure
- decomposition 오류
- 근거 없이 기능을 과대평가한 지점
- custom build를 너무 쉽게 추천한 지점 / 반대로 custom gap을 놓친 지점

결과 표:

| Case | Skill 판단 | 사람의 사후 판단 | 일치 여부 | 주요 실패 |
|---|---|---|---|---|

## 작업 종료 시 반드시 답할 질문

1. 이 문제는 Claude Skill만으로 충분히 해결되는가?
2. 충분하지 않다면 가장 큰 failure는 무엇인가?
3. 그 failure는 prompt 개선만으로 해결 가능한가?
4. Semantic Retrieval / RAG가 필요한 실제 근거가 발견됐는가?
5. Agentic Search가 필요한 실제 근거가 발견됐는가?
6. Reranker가 필요한 실제 근거가 발견됐는가?
7. 별도 Backend가 필요한 이유가 명확한가?
8. 별도 Frontend가 제공하는 가치가 명확한가?
9. 최종 추천: Skill로 유지 / Skill 개선 / 별도 제품 PoC 진행 / 아이디어 폐기

## 제품화 조건 (참고)

**판정 규칙(명확화)**: 아래 failure 유형 중 **서로 다른 2개 이상의 유형이 각각 2회 이상 반복**되고, 그 failure가 **복구되지 않아 최종 판정을 실제로 바꿨거나 바꿀 뻔했을 때**만 별도 제품 PoC를 검토한다. 복구된 failure(예: web 확대로 발견)는 반복 횟수에는 세되 "판단 영향" 요건을 충족하지 못한다.

**집계 절차**: failure로 세려면 ground truth(해결책 실존 증거 URL 또는 실존 확인 방법)가 있어야 한다. 카탈로그 빈 결과는 ground truth 없이는 true negative일 수 있으므로 집계하지 않고 "후보"로만 기록한다.

**gold label 재검증**: 각 케이스의 "예상 비교 기준"은 작성 시점의 가설이며 노후화될 수 있다(Case 2에서 실증 — culling 전용 제품군 미반영). 사람 사후판단 작성 시 예상 기준 자체의 오류 여부를 별도 컬럼으로 기록한다.

**블라인드 권고**: 이 문서(관찰 항목 포함)를 실행 컨텍스트에 넣지 말고, 입력 문구만 전달해 실행한다. 관찰 항목이 컨텍스트에 있으면 분석 축이 사전 결정되는 누출이 실증됐다.

1. **Semantic Retrieval Failure** — 표현 차이로 기존 솔루션을 못 찾음 → capability-level semantic index 필요 가능성
2. **Capability Verification Failure** — 도구는 찾았지만 실제 기능을 잘못 판단 → README/docs evidence verification 필요
3. **Composition Failure** — 조합하면 해결되는데 단일 제품만 찾음 → multi-tool composition reasoning 필요
4. **Agentic Exploration 필요** — 검색→문서 확인→재탐색→검증→재검색의 iterative search가 반복 → Agent 구조 검토
5. **실행 기반 평가 필요** — "될 것 같다"와 실제 task 성공의 차이가 큼 → Prompt-only / Tool-enabled / Skill / Custom workflow를 실제 실행 비교하는 Evaluation Backend 검토
6. **비용/성능/프라이버시 비교 필요** — 비용, latency, privacy, local/cloud, 유지보수, 정확도 trade-off가 중요 → 구조화된 비교 시스템 검토

Vector DB, Reranker, Agent, Backend, Frontend는 지금 구현하지 않는다. **실제 failure가 근거가 될 때만 도입한다.**
