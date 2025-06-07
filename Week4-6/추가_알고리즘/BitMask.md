# 📝 비트 마스크(Bitmask) 알고리즘 정리

## 1. 비트 마스크란?

비트 마스크는 **정수를 이진수 형태로 해석하여**, **각 비트(bit)의 상태(0 또는 1)** 를 통해 **여러 상태를 동시에 표현하거나 처리**하는 알고리즘 기법이다.

주로 다음과 같은 상황에 사용된다:

- 원소의 **선택 여부**를 표현할 때
- **부분 집합을 탐색**하거나
- **상태를 압축**해서 동적 계획법(DP)에 활용할 때

---

## 2. 비트 마스크의 장단점

### 장점
- 수행 시간이 빠르다
- 메모리 사용량이 적다

### 단점
- 직관성이 떨어진다

---

## ⚙️ 주요 연산

| 연산 유형           | 표현 방식                  | 설명                                      |
|---------------------|----------------------------|-------------------------------------------|
| i번 원소가 포함?   | `mask & (1 << i)`          | i번째 비트가 1인지 확인                   |
| i번 원소 추가        | `mask \| (1 << i)`          | i번째 비트를 1로 설정                     |
| i번 원소 제거        | `mask & ~(1 << i)`         | i번째 비트를 0으로 설정                   |
| i번 원소 반전(toggle) | `mask ^ (1 << i)`          | i번째 비트를 0 → 1 또는 1 → 0으로 반전    |
| 모든 부분 집합 순회 | `for mask in range(1 << N)`| 0부터 2^N-1까지 순회                      |

---

## 3. 코드

```python
def get_all_shortest_distances(graph, n):
    """
    모든 장소 쌍 간의 최단 거리를 계산 (플로이드-워셜의 다익스트라 버전)
    
    Returns:
        all_distances[i][j]: i번 장소에서 j번 장소까지의 최단 거리
    """
    all_distances = []

    # 각 장소를 시작점으로 하여 다익스트라 실행
    for start_node in range(n):
        distances = dijkstra(graph, start_node, n)
        all_distances.append(distances)
    
    return all_distances

# 🗺️ 모든 장소 간 최단 거리 계산
dist = get_all_shortest_distances(graph, N)

# 🎯 === 동적 계획법 + 비트마스크 ===

INF = float('inf')

# dp[mask][i]: 작업 완료 상태가 mask이고 i번 장소에 있을 때의 최소 소요시간
# mask의 j번째 비트가 1이면 j번 작업을 완료했다는 의미
dp = [[INF] * N for _ in range(1 << N)]

# 📍 경로 추적을 위한 부모 상태 저장
# parent[mask][i] = (이전_mask, 이전_위치, 행동_타입, 대상)
parent = [[None] * N for _ in range(1 << N)]

# 🏠 시작점: 집(0번 장소)에서 아무 작업도 완료하지 않은 상태
dp[0][0] = 0

def can_visit(mask, job):
    """
    현재 완료한 작업들(mask)로 job 작업을 수행할 수 있는지 선행조건 확인
    
    Args:
        mask: 현재까지 완료한 작업들의 비트마스크
        job: 수행하려는 작업 번호
    
    Returns:
        bool: 선행조건을 모두 만족하면 True
    """
    for prereq_job in prereq[job]:
        if not (mask & (1 << prereq_job)):  # 선행과목이 완료되지 않음
            return False
    return True

# 🔄 === 비트마스크 동적계획법 실행 ===

for mask in range(1 << N):
    for current in range(N):
        # 현재 상태가 도달 불가능하면 건너뛰기
        if dp[mask][current] == INF:
            continue
            
        # 🛠️ **액션 1**: 현재 장소에서 일을 수행
        if not (mask & (1 << current)) and can_visit(mask, current):
            work_time = times[current]
            
            # 작업 시간이 제한시간을 초과하지 않는 경우
            if dp[mask][current] + work_time <= T:
                new_mask = mask | (1 << current)  # 현재 작업을 완료 상태로 변경
                new_time = dp[mask][current] + work_time
                
                # 더 빠른 방법으로 같은 상태에 도달 가능한지 확인
                if new_time < dp[new_mask][current]:
                    dp[new_mask][current] = new_time
                    parent[new_mask][current] = (mask, current, "work", current)
        
        # 🚶 **액션 2**: 다른 장소로 이동
        for next_place in range(N):
            if current != next_place and dist[current][next_place] != INF:
                travel_time = dist[current][next_place]
                
                # 이동 시간이 제한시간을 초과하지 않는 경우
                if dp[mask][current] + travel_time <= T:
                    new_time = dp[mask][current] + travel_time
                    
                    # 더 빠른 방법으로 같은 상태에 도달 가능한지 확인
                    if new_time < dp[mask][next_place]:
                        dp[mask][next_place] = new_time
                        parent[mask][next_place] = (mask, current, "move", next_place)

# 🏆 === 최적해 탐색 (집으로 돌아와야 함) ===

max_score = 0
best_mask = 0
best_location = 0

for mask in range(1 << N):
    for current in range(N):
        if dp[mask][current] == INF:
            continue
            
        # 현재 위치에서 집(0번 장소)으로 돌아가는 시간 계산
        if current == 0:
            return_time = 0  # 이미 집에 있음
        else:
            return_time = dist[current][0]  # 현재 위치에서 집으로 가는 시간
        
        # 집으로 돌아갈 수 있는 시간이 남아있는지 확인
        if dp[mask][current] + return_time <= T:
            # 현재 상태에서 획득할 수 있는 총 점수 계산
            score = 0
            for i in range(N):
                if mask & (1 << i):  # i번째 일을 완료했다면
                    score += scores[i]
            
            # 최고 점수 갱신
            if score > max_score:
                max_score = score
                best_mask = mask
                best_location = current
```
---
