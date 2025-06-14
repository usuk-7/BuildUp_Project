# 📝 비트 마스크(Bitmask) 알고리즘 정리

## 1. 비트 마스크란?

비트 마스크는 **정수를 이진수 형태로 해석하여**, **각 비트(bit)의 상태(0 또는 1)** 를 통해 **여러 상태를 동시에 표현하거나 처리**하는 알고리즘 기법이다.

주로 다음과 같은 상황에 사용된다:

- 원소의 **선택 여부**를 표현할 때
- **부분 집합을 탐색**하거나
- **상태를 압축**해서 동적 계획법(DP)에 활용할 때

---

## 2. 비트 마스크의 장단점

| 장점 | 설명 |
|------|------|
| 메모리 절약 | 여러 상태를 하나의 정수로 표현해 배열보다 메모리를 적게 사용 |
| 빠른 연산 속도 | 비트 연산은 매우 빠르며 상태 확인과 변경이 O(1) |
| DP 최적화에 유용 | 집합을 상태로 표현하는 DP에서 효과적 (예: TSP 문제) |

| 단점 | 설명 |
|------|------|
| 비트 수 제한 | 상태 수가 2으로 증가, 일반적으로 n ≤ 20~25가 한계 |
| 가독성 저하 | 비트 연산이 익숙하지 않으면 코드 해석이 어려움 |
| 디버깅 어려움 | 0b101010 같은 상태를 직관적으로 해석하기 어려움 |


---

## 3. 사용 예시

| 분야       | 설명                        |
| -------- | ------------------------- |
| 부분 집합 탐색 | 2^N개 조합 탐색 시 유용           |
| DP 최적화   | `dp[mask][pos]` 형태로 상태 저장 |
| 퍼즐/게임 상태 | 완성된 조각 관리                 |
| 그래프 순회   | 방문 노드 집합 관리               |
| 최적화 문제   | TSP, 최소 점프, 최소 연산 횟수 등    |

---

## ⚙️ 주요 자료구조

| 자료구조               | 설명                             |
| ------------------ | ------------------------------ |
| `int mask`         | N개의 상태를 2진수로 압축 표현 (`0~2^N-1`) |
| `1 << i`           | i번째 비트만 1인 값 생성  |
| `mask & (1 << i)`  | i번 상태가 포함되었는지 확인  |
| `mask \| (1 << i)` | i번 상태를 추가 |
| `mask & ~(1 << i)` | i번 상태를 제거 |
| `mask ^ (1 << i)`  | i번 상태 반전 (0 → 1, 1 → 0) |


---

## 4. 시간 복잡도 비교

| 방법       | 시간 복잡도               | 상태 수   |
| -------- | -------------------- | ------ |
| 일반 조합 탐색 | O(2^N × N)           | O(2^N) |
| 비트마스크 사용 | O(2^N) or O(2^N × N) | O(2^N) |

## 추가 예시 코드

### 가능한 모든 부분집합의 합 계산

```python
arr = [3, 1, 4]       # 원소가 3, 1, 4인 리스트
n = len(arr)          # 리스트의 길이, 원소 개수

for mask in range(1 << n):  # 0부터 2^n - 1까지 모든 비트마스크 순회 (부분집합 모든 경우)
    subset = []         # 현재 비트마스크에 해당하는 부분집합 원소들을 담을 리스트
    total = 0           # 부분집합 원소들의 합을 저장할 변수

    for i in range(n):  # 각 원소 위치에 대해
        if mask & (1 << i):  # 비트마스크의 i번째 비트가 1이면 (i번째 원소가 포함된 경우)
            subset.append(arr[i])  # i번째 원소를 부분집합에 추가
            total += arr[i]         # 합에 i번째 원소 더하기

    print(f"{subset} → 합: {total}")  # 현재 부분집합과 합 출력
```

## 출력 예시

```python
[] → 합: 0
[3] → 합: 3
[1] → 합: 1
[3, 1] → 합: 4
[4] → 합: 4
[3, 4] → 합: 7
[1, 4] → 합: 5
[3, 1, 4] → 합: 8
```

## 결론

비트 마스크는 복잡한 상태나 조합을 정수 하나로 표현하는 강력한 기법이다. 특히 원소 선택, 방문 여부, 집합 상태 등을 빠르게 처리할 수 있어, 탐색과 동적 계획법에서 시간과 메모리를 절약하는 데 필수적이다.

---
