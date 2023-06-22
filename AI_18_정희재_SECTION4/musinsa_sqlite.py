import sqlite3

# 데이터를 담을 리스트
data = []

# 데이터 파일 열기
with open('musinsa_snap_data.csv', 'r') as file:
    next(file)  # 첫 번째 행은 헤더이므로 건너뜁니다.
    for line in file:
        age, category, count = line.strip().split(',')
        data.append((age, category, int(count)))  # 데이터 리스트에 튜플 추가

conn = sqlite3.connect('musinsa_snap.db')
cur = conn.cursor()

# 테이블 생성
cur.execute('''
    CREATE TABLE fashion_data (
        age_group TEXT,
        category TEXT,
        count INTEGER
    )
''')

# 데이터 삽입
cur.executemany('''
    INSERT INTO fashion_data (age_group, category, count) VALUES (?, ?, ?)
''', data)

# 변경 사항 커밋
conn.commit()

# 연결 종료
conn.close()