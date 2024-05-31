## 기본 세팅
<!--python --version이 2.x인 경우, 더이상 지원되지 않음!
이런 경우, python 3.x.x버전을 다운받고 pip3로 다운받기-->

pip install -q -U google-generativeai

pip install ipython​

pip install mysql-connector-python

pip install python-dotenv

<!-- 다운 받고 시작!! -->

=======
그럼 가상 환경에서 ai 파일이 돌아가게 됨.

- gemini api 페이지에서 본인 api key 받아서 넣으면 됨!

## 주의

영화 시놉시스가 아래와 같은 내용을 담고 있으면 예외 발생함.

- HARM_CATEGORY_SEXUALLY_EXPLICIT: 성적으로 노골적인 콘텐츠
- HARM_CATEGORY_HATE_SPEECH: 증오 발언
- HARM_CATEGORY_HARASSMENT: 괴롭힘
- HARM_CATEGORY_DANGEROUS_CONTENT: 위험한 콘텐츠
