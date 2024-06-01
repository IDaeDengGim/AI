import pathlib
import textwrap
import google.generativeai as genai
import os
import mysql.connector

from IPython.display import Markdown

from dotenv import dotenv_values

# Load environment variables from .env file
env_values = dotenv_values('.env')


# 서식이 지정된 Markdown 텍스트를 표시하는 함수
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

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
query = "SELECT id, synopsys, intent FROM movie WHERE id BETWEEN 1 AND 5"
cursor.execute(query)
movies = cursor.fetchall()

# ai_tag 테이블 생성 (없다면)
create_table_query = """
CREATE TABLE IF NOT EXISTS ai_tag (
    id INT PRIMARY KEY,
    tag VARCHAR(255),
    genre TEXT
)
"""

cursor.execute(create_table_query)

# Gemni API를 사용하여 태그와 장르 추출 및 저장
for movie in movies:
    movie_id, synopsys, intent = movie
    input_text = f"{synopsys} {intent}"

    chat = model.start_chat(history=[])
    
    try:
        response_tag = chat.send_message(input_text + ":다음은 영화에 관한 설명이야. 영화를 설명할 수 있는 주요 키워드 3개를 comma로 구분해서 알려줘. 결과값은 한국어로 부탁해.")
        tags = response_tag.text.strip()

        response_genre = chat.send_message(input_text + ":이 시놉시스로 미루어볼때 어떤 장르의 영화같아? 장르 2개를 comma로 구분해서 알려줘. 결과값은 한국어로 부탁해.")
        genres = response_genre.text.strip()

        # 결과를 ai_tag 테이블에 저장
        insert_query = "INSERT INTO ai_tag (id, tag, genre) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE tag=%s, genre=%s"
        cursor.execute(insert_query, (movie_id, tags, genres, tags, genres))

        print(str(movie_id)+") Tags:", tags)
        print("Genres:", genres)
    
    except genai.types.generation_types.StopCandidateException as e:
        print(str(movie_id)+": An error occurred") # error 처리
        continue
    
# 변경사항 커밋 및 MySQL 연결 종료
conn.commit()
cursor.close()
conn.close()
