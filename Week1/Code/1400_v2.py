import heapq
import sys

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
    """
    다익스트라 알고리즘을 이용한 최단 경로 탐색
    
    📍 **1400_v2.py vs 1400.py 차이점 2**: 지역 변수 사용 (함수 독립성 ↑)
    """
    # 📍 **개선점**: 전역 변수 대신 지역 변수 사용
    rows = len(Map)
    columns = len(Map[0])
    
    # 최단 시간 저장 배열 초기화
    seen = [[float('inf') for _ in range(columns)] for _ in range(rows)]

    # 시작점 A 찾기
    ar, ac = None, None
    for i in range(rows):
        for j in range(columns):
            if Map[i][j] == 'A':
                ar, ac = i, j
                break
        if ar is not None:
            break

    # ✅ **1400_fail.py 대비 개선점**: A를 찾지 못한 경우 처리
    if ar is None:
        return -1

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
            if 0 <= ni < rows and 0 <= nj < columns and isValid(Map[ni][nj]):
                cell_type = Map[ni][nj]
                
                # ✅ **1400_fail.py 대비 개선점**: 조건별 분기 처리
                if cell_type.isdigit():
                    # 신호등인 경우
                    light_num = int(cell_type)
                    if light_num < len(t_lights) and t_lights[light_num] is not None:
                        light_dir, ew, ns = t_lights[light_num]
                        next_time = entryTime(t, direction, light_dir, ew, ns)
                    else:
                        # 신호등 정보가 없는 경우
                        next_time = t + 1
                else:
                    # 신호등이 아닌 경우 바로 진입
                    next_time = t + 1

                # 더 빠른 경로를 발견한 경우 업데이트
                if next_time < seen[ni][nj]:
                    seen[ni][nj] = next_time
                    heapq.heappush(pq, (next_time, ni, nj))

    # B에 도달할 수 없는 경우
    return -1

def main():
    """
    메인 함수 - sys.stdin을 이용한 배치 입력 처리
    
    📍 **1400_v2.py vs 1400.py 차이점 3**: 배치 입력 처리 (복잡하지만 안정적)
    """
    
    # 📍 **입력 방식 1**: 모든 입력을 한 번에 읽어서 배열로 저장
    # 장점: 입력 순서 제어 용이, 복잡한 파싱에 유리
    # 단점: 메모리 사용량 증가, 코드 복잡도 증가
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    i = 0  # 현재 처리 중인 줄 인덱스
    
    while i < len(lines):
        # 빈 줄 건너뛰기
        if not lines[i]:
            i += 1
            continue
            
        # 지도 크기 입력
        m, n = map(int, lines[i].split())
        i += 1
        
        if m == 0 and n == 0:
            break
        
        # 📍 **입력 방식 2**: 배열에서 순차적으로 읽기
        # 지도 정보 읽기
        Map = []
        for _ in range(m):
            if i < len(lines):
                Map.append(lines[i])
                i += 1
        
        # ✅ **1400_fail.py 대비 개선점**: 고정 크기 배열로 신호등 저장
        # 📍 **1400_v2.py vs 1400.py 차이점 4**: 고정 배열 vs 동적 리스트
        t_lights = [None] * 10  # 0-9까지의 신호등을 위한 고정 크기 리스트
        
        # 신호등 정보 읽기
        while i < len(lines):
            if not lines[i]:  # 빈 줄이면 신호등 입력 종료
                i += 1
                break
                
            parts = lines[i].split()
            
            # 📍 **복잡한 입력 처리**: 다음 테스트 케이스 시작 감지
            # 다음 테스트 케이스의 시작인지 확인 (m, n 형태)
            if len(parts) == 2:
                try:
                    int(parts[0])
                    int(parts[1])
                    # 다음 테스트 케이스이므로 현재 줄은 처리하지 않고 종료
                    break
                except:
                    pass
            
            # 신호등 정보 파싱
            if len(parts) == 4:
                try:
                    index = int(parts[0])
                    d = parts[1]
                    ew = int(parts[2])
                    ns = int(parts[3])
                    
                    # ✅ **1400_fail.py 대비 개선점**: 인덱스 기반 저장
                    if 0 <= index < 10:
                        t_lights[index] = (d, ew, ns)
                except:
                    pass
            
            i += 1
        
        # 최단 경로 계산
        time = drive(Map, t_lights)
        
        # 결과 출력
        if time > 0:
            print(time)
        else:
            print('impossible')

if __name__ == '__main__':
    main()

"""
📋 **1400_v2.py의 특징 (vs 1400.py 비교)**:

✅ **장점**:
1. 지역 변수 사용 - 함수 독립성 향상
2. 배치 입력 처리 - 복잡한 입력 상황에 안정적
3. 고정 크기 배열 - 메모리 예측 가능
4. 전체 입력 제어 - 파싱 로직 자유도 높음

⚠️ **단점**:
1. 메모리 사용량 증가 - 모든 입력을 메모리에 저장
2. 코드 복잡도 증가 - 이해하기 어려움
3. 일반적이지 않은 입력 처리 방식

🔧 **1400_fail.py에서 수정된 점**:
1. UnboundLocalError 해결 (조건별 분기)
2. 신호등 인덱스 문제 해결
3. A 찾기 실패 처리 추가
4. 복잡한 입력 파싱 로직 추가

📊 **1400.py vs 1400_v2.py 선택 기준**:
- 단순한 문제: 1400.py (표준 input() 방식)
- 복잡한 입력: 1400_v2.py (sys.stdin 방식)
- 코딩테스트: 1400.py 권장
- 실제 개발: 상황에 따라 선택
"""