import pathlib
import textwrap
 
import google.generativeai as genai
 
from IPython.display import display
from IPython.display import Markdown

# 서식이 지정된 Markdown 텍스트를 표시하는 함수
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
 
# 제미나이 API 키 설정
genai.configure(api_key="본인 api key 입력")


# 모델 설정
model = genai.GenerativeModel('gemini-pro') # 텍스트 전용 모델

# 실시간 텍스트 생성
# response = model.generate_content("사과는 어떻게 생겼어? 한국말로 답해줘").text

# print(response)

# 대화내용 자동 저장
chat = model.start_chat(history=[])

q1 = input("영화의 줄거리를 입력하세요: ") 
 
# 첫 번째 질문 내용에 대한 답변 응답
response = chat.send_message(q1 + "의 가장 중요한 키워드 3개를 한국어로 뽑아줘. 참고로 영화에 대한 줄거리야.")
print("----------------------------------------")
print(response.text)
print("----------------------------------------")

response2 = chat.send_message(q1 + "이 시놉시스로 미루어볼때 어떤 장르의 영화같아? 한국어로 2개만 뽑아줘.")
print(response2.text)
print("----------------------------------------")
