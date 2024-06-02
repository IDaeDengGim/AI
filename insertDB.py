import google.generativeai as genai
import google.api_core.exceptions
import mysql.connector
import time

from IPython.display import Markdown
from dotenv import dotenv_values

# Load environment variables from .env file
env_values = dotenv_values('.env')

# .env에서 정보 가져오기
GEMINI_API_KEY = env_values.get("GEMINI_API_KEY")
DB_USER = env_values.get("DB_USER")
DB_PW = env_values.get("DB_PASSWORD")
DB_HOST = env_values.get("DB_HOST")
DB_NAME = env_values.get("DB_NAME")

# 제미나이 API 키 설정
genai.configure(api_key=GEMINI_API_KEY)

# 모델 설정
model = genai.GenerativeModel('gemini-pro') # 텍스트 전용 모델

# MySQL 데이터베이스 연결 설정
db_config = {
    'user': DB_USER,
    'password': DB_PW,
    'host': DB_HOST,
    'database': DB_NAME,
    'port':3306
}

# MySQL 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 영화 데이터 가져오기
query = "SELECT id, synopsys, intent FROM movie WHERE id BETWEEN 101 AND 150"
cursor.execute(query)
movies = cursor.fetchall()

# tags 테이블 생성 
# create_table_query = """
# CREATE TABLE IF NOT EXISTS tags (
#     id LONG PRIMARY KEY,
#     tag_name VARCHAR(255)
# )
# """
# cursor.execute(create_table_query)

# 프롬프트 설정
tag_prompt = ":다음은 영화에 관한 설명이야. 영화를 설명할 수 있는 주요 키워드 2~3개를 ','로 구분해서 알려줘. 결과값은 한국어로 부탁해."
genre_prompt = ":이 시놉시스로 미루어볼때 어떤 장르의 영화같아? 장르 2개를 ','로 구분해서 알려줘. 결과값은 한국어로 부탁해."

# Gemni API를 사용하여 태그와 장르 추출 및 저장
for movie in movies:
    movie_id, synopsys, intent = movie
    input_text = f"{synopsys} {intent}"

    chat = model.start_chat(history=[])
    error_count = 0 # 오류 3번 이상 발생 시 다음 영화로 넘어가기
    
    while True:
        try:
            # tag 추출
            response_tag = chat.send_message(input_text + tag_prompt)
            tags = [tag.strip() for tag in response_tag.text.strip().split(",")]

            # tags 테이블에 INSERT
            for tag in tags:
                insert_query = "INSERT INTO tag (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=%s"
                cursor.execute(insert_query, (tag,tag))
                
            # genre 추출  
            response_genre = chat.send_message(input_text + genre_prompt)
            genres = [genre.strip() for genre in response_genre.text.strip().split(",")]

            # genres 테이블에 INSERT
            for genre in genres:
                insert_query = "INSERT INTO genre (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=%s"
                cursor.execute(insert_query, (genre, genre))
                
            # INSERT한 tags, genres에서 id 가져오기
            select_query = f"SELECT id FROM tag WHERE name IN ({','.join(['%s']*len(tags))})"
            cursor.execute(select_query, tuple(tags))
            tag_ids = [row[0] for row in cursor.fetchall()]

            select_query = f"SELECT id FROM genre WHERE name IN ({','.join(['%s']*len(genres))})"
            cursor.execute(select_query, tuple(genres))
            genre_ids = [row[0] for row in cursor.fetchall()]

            # movie_tag 테이블에 INSERT (movie와 tag의 관계)
            for tag_id in tag_ids:
                insert_query = "INSERT INTO movie_tag (movie_id, tag_id) VALUES (%s, %s)"
                cursor.execute(insert_query, (movie_id, tag_id))

            # movie_genre 테이블에 INSERT (movie와 genre의 관계)
            for genre_id in genre_ids:
                insert_query = "INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)"
                cursor.execute(insert_query, (movie_id, genre_id))
                
            print(f"{movie_id}) Tags:", tags)
            print("Genres:", genres)
            
            time.sleep(2)  # 2초 대기
            break  # 처리 완료 -> 루프 종료
        
        except genai.types.generation_types.StopCandidateException as e: # 시놉시스 input에 따른 예외
            print(f"{movie_id}: An error occurred")  # error 처리
            error_count+=1
            if(error_count>=3): break
            else: time.sleep(2) # 2초 후 재시도
        
        except google.api_core.exceptions.ResourceExhausted as e: # api 사용량 초과
            print("Quota exceeded. Retrying...")
            error_count+=1
            if(error_count>=3): break
            else: time.sleep(5) # 5초 후 재시도
    
    
# 변경사항 커밋 및 MySQL 연결 종료
conn.commit()
cursor.close()
conn.close()
