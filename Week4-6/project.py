"""
🏠 **하루 일정 최적화 도우미**

📋 **문제 설명**:
- N개의 장소에서 수행할 일들이 있고, 각각 중요도 점수와 소요시간이 주어짐
- 일부 일은 선행 조건이 있어서 다른 일을 먼저 완료해야 수행 가능
- 장소 간 이동에는 시간이 소요되며, 시작과 끝은 반드시 0번 장소(집)
- 제한시간 T 내에서 최대 중요도 점수를 얻는 일정 계획

🧠 **알고리즘**:
1. 다익스트라: 모든 장소 간 최단 이동시간 계산
2. 비트마스크 DP: 완료한 작업 상태를 비트로 표현
3. 경로 추적: 최적 해의 구체적인 수행 순서 복원

⏰ **시간 복잡도**: O(N³ + N² × 2^N)
💾 **공간 복잡도**: O(N² + N × 2^N)
"""

# 📥 === 입력 데이터 처리 ===

# 장소 수(N), 간선 수(M), 최대 시간(T)
N, M, T = map(int, input().split())

# 각 장소에서 수행할 일의 중요도 점수 (0번은 집이므로 0점)
scores = list(map(int, input().split()))

# 각 장소에서 일을 완료하는데 필요한 작업 시간 (0번은 집이므로 0분)
times = list(map(int, input().split()))

# 🗺️ 그래프 초기화: graph[a] = [(b, t), ...] (a→b로 가는데 t분 소요)
graph = [[] for _ in range(N)]

# 장소 간 이동 경로 정보 입력
for _ in range(M):
    a, b, t = map(int, input().split())
    graph[a].append((b, t))

# 📋 선수 작업 정보 처리
K = int(input())

# prereq[x] = {y1, y2, ...}: x번 일을 하려면 y1, y2, ... 일을 먼저 완료해야 함
prereq = [set() for _ in range(N)]
for _ in range(K):
    x, y = map(int, input().split())
    prereq[x].add(y)

# 🚀 === 다익스트라 알고리즘 ===

import heapq

def dijkstra(graph, start, n):
    """
    시작점에서 모든 다른 장소까지의 최단 거리를 계산
    
    Args:
        graph: 인접 리스트로 표현된 그래프
        start: 시작 장소 번호
        n: 전체 장소 개수
    
    Returns:
        distances: start에서 각 장소까지의 최단 거리 배열
    """
    # 🎯 거리 배열 초기화 (무한대로 설정)
    distances = [float('inf')] * n
    distances[start] = 0

    # 우선순위 큐: (거리, 노드)
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # 이미 처리된 노드는 건너뛰기 (더 짧은 경로가 이미 발견됨)
        if current_dist > distances[current_node]:
            continue

        # 현재 노드에서 인접한 모든 노드 확인
        for next_node, travel_time in graph[current_node]:
            new_dist = current_dist + travel_time

            # 더 짧은 경로를 발견한 경우 업데이트
            if new_dist < distances[next_node]:
                distances[next_node] = new_dist
                heapq.heappush(pq, (new_dist, next_node))
    
    return distances

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

# 📍 === 경로 역추적 함수 ===

def reconstruct_path(mask, location):
    """
    최적해의 구체적인 행동 순서를 역추적하여 복원
    
    Args:
        mask: 최종 작업 완료 상태
        location: 최종 위치
    
    Returns:
        path: 수행한 행동들의 순서 리스트
    """
    path = []
    current_mask = mask
    current_loc = location
    
    # 부모 상태를 따라가면서 경로 복원
    while parent[current_mask][current_loc] is not None:
        prev_mask, prev_loc, action_type, target = parent[current_mask][current_loc]
        
        if action_type == "work":
            path.append(f"장소 {current_loc}에서 작업 {target} 수행")
        elif action_type == "move":
            path.append(f"장소 {prev_loc}에서 장소 {current_loc}로 이동")
            
        current_mask = prev_mask
        current_loc = prev_loc
    
    path.reverse()  # 역순으로 쌓였으므로 뒤집기
    return path

# 📤 === 결과 출력 ===

print(max_score)

if max_score > 0:
    print("\n=== 최적 경로 ===")
    path = reconstruct_path(best_mask, best_location)
    
    print("시작: 장소 0")
    for step in path:
        print(step)
    
    # 🏠 집으로 복귀
    if best_location != 0:
        print(f"장소 {best_location}에서 장소 0으로 이동 (복귀)")
    
    print("\n=== 완료한 작업들 ===")
    completed_jobs = []
    total_score = 0
    for i in range(N):
        if best_mask & (1 << i):
            completed_jobs.append(i)
            total_score += scores[i]
    
    for job in completed_jobs:
        print(f"작업 {job}: 점수 {scores[job]}, 소요시간 {times[job]}")
    
    print(f"\n총 점수: {total_score}")
    print(f"총 소요시간: {dp[best_mask][best_location] + (dist[best_location][0] if best_location != 0 else 0)}")
else:
    print("시간 내에 완료할 수 있는 작업이 없습니다.")

"""
🔍 **알고리즘 동작 과정**:

1️⃣ **전처리**: 
   - 다익스트라로 모든 장소 쌍 간 최단거리 계산: O(N³)
   - 선행조건 정보를 집합으로 저장

2️⃣ **DP 상태 정의**:
   - dp[mask][i]: 작업 완료 상태가 mask이고 i번 장소에 있을 때의 최소 시간
   - mask: N비트로 각 작업의 완료 여부 표현

3️⃣ **상태 전이**:
   - 작업 수행: 선행조건 만족 시 현재 장소에서 작업 완료
   - 장소 이동: 다른 장소로 이동 (최단거리 사용)

4️⃣ **최적해 탐색**:
   - 모든 완료 상태에서 집으로 돌아갈 수 있는 경우 중 최고 점수 선택

5️⃣ **경로 복원**:
   - parent 배열을 이용해 최적해의 구체적인 행동 순서 추적

🎯 **핵심 아이디어**:
- 비트마스크로 작업 완료 상태를 효율적으로 관리
- DP로 중복 계산 방지하며 모든 가능한 경우 탐색
- 선행조건과 시간 제약을 동시에 고려한 상태 전이
"""
