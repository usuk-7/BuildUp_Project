import heapq

EW, NS = 0, 1

def isValid(Type):
    """벽('.')이 아닌 모든 셀은 유효함 - 벽 검사 함수"""
    return Type != '.'

def entryTime(t, d, Type, ew, ns):
    """
    신호등이 있는 교차로에 진입하는 시간 계산
    
    Parameters:
    - t: 현재 시간
    - d: 진입 방향 (EW=0: 동서, NS=1: 남북)
    - Type: 신호등 타입 ('-': 동서만, '|': 남북만)
    - ew: 동서 방향 신호 지속 시간 (1~20)
    - ns: 남북 방향 신호 지속 시간 (1~20)
    """
    if Type == '-':  # 동서 방향만 통과 가능한 신호등
        r = t % (ew + ns)
        if d == EW and r >= ew:
            t += (ew + ns - r)
        if d == NS and r < ew:
            t += (ew - r)
    elif Type == '|':  # 남북 방향만 통과 가능한 신호등
        r = t % (ew + ns)
        if d == EW and r < ns:
            t += (ns - r)
        if d == NS and r >= ns:
            t += (ns + ew - r)
    return t + 1

def drive(Map, t_lights):
    """다익스트라 알고리즘을 이용한 최단 경로 탐색"""
    global m, n
    
    # 최단 시간 저장 배열 초기화
    seen = [[float('inf') for _ in range(n)] for _ in range(m)]

    # 시작점 A 찾기 - 문제 조건상 A는 항상 존재
    ar, ac = 0, 0
    for i in range(m):
        for j in range(n):
            if Map[i][j] == 'A':
                ar, ac = i, j
                break
        if Map[i][j] == 'A':
            break

    # 우선순위 큐 초기화 (시간, 행, 열)
    pq = [(0, ar, ac)]
    seen[ar][ac] = 0

    # 다익스트라 알고리즘 실행
    while pq:
        t, i, j = heapq.heappop(pq)

        # 목적지 B에 도달한 경우
        if Map[i][j] == 'B':
            return t

        # 이미 더 빠른 경로로 방문한 경우 건너뛰기
        if t > seen[i][j]:
            continue

        # 상하좌우 네 방향 탐색
        directions = [(0, -1, EW), (0, 1, EW), (-1, 0, NS), (1, 0, NS)]

        for di, dj, direction in directions:
            ni, nj = i + di, j + dj

            # 지도 범위 내이고 유효한 셀인지 확인
            if 0 <= ni < m and 0 <= nj < n and isValid(Map[ni][nj]):
                cell_type = Map[ni][nj]
                ew, ns = 0, 0  # 기본값 설정

                if cell_type.isdigit():
                    idx = int(cell_type)
                    # 문제 조건상 신호등 정보는 항상 존재하지만 안전을 위해 체크
                    if idx < len(t_lights) and t_lights[idx] is not None:
                        cell_type, ew, ns = t_lights[idx]

                # 다음 시간 계산
                next_time = entryTime(t, direction, cell_type, ew, ns)

                # 더 빠른 경로를 발견한 경우 업데이트
                if next_time < seen[ni][nj]:
                    seen[ni][nj] = next_time
                    heapq.heappush(pq, (next_time, ni, nj))

    # B에 도달할 수 없는 경우
    return -1

def main():
    """
    메인 함수 - 문제 조건이 완벽하게 보장되는 간소화된 버전
    
    🎯 가정:
    - 모든 입력은 올바른 형식
    - "0 0"으로 정상 종료 보장
    - 빈 줄로 신호등 정보 구분 보장
    - 모든 숫자는 정수 형태
    """
    global m, n

    while True:
        # 지도 크기 입력 - 문제 조건상 항상 올바른 형식
        m, n = map(int, input().split())
        if m == 0 and n == 0:
            break

        # 지도 정보 입력 - 문제 조건상 정확히 m줄
        Map = []
        for _ in range(m):
            Map.append(input().strip())

        # 신호등 정보 저장 - 동적 리스트 사용
        t_lights = []

        # 신호등 정보 읽기 - 빈 줄까지 읽음
        while True:
            line = input().strip()
            if not line:  # 빈 줄이면 신호등 입력 종료
                break

            # 신호등 정보 파싱 - 문제 조건상 항상 올바른 형식
            parts = line.split()
            index = int(parts[0])
            d = parts[1]
            ew = int(parts[2])
            ns = int(parts[3])

            # 리스트 크기를 동적으로 확장
            while len(t_lights) <= index:
                t_lights.append(None)

            # 올바른 인덱스에 저장
            t_lights[index] = (d, ew, ns)

        # 최단 경로 계산
        time = drive(Map, t_lights)

        # 결과 출력
        if time > 0:
            print(time)
        else:
            print('impossible')

if __name__ == '__main__':
    main()