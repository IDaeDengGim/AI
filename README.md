# IndiePIcks

## 👩‍💻 AI 

|💚|💚|
|:---:|:---:|
|[김근주](https://github.com/tdddt)| [김현수](https://github.com/SSSSSSu3834)|
| DB 연결 | 초기 세팅 |

</br>

## ✏️  개요
Gemini API를 활용해 영화 시나리오를 토대로 키워드와 장르를 추출한다.

</br>

## 📒 파일 설명
`insertDB.py` : DB에 추출한 키워드와 장르를 저장하기 위한 파일

`testPrompt.py` : 프롬프팅 성능 테스트를 위한 파일

`.env` : DB 보안 관련 파일

</br>


## 📦 라이브러리

`google-generativeai` 

`mysql-connector-python`

`python-dotenv`


</br>

## Installation

### 기본 세팅
<!--python --version이 2.x인 경우, 더이상 지원되지 않음!
이런 경우, python 3.x.x버전을 다운받고 pip3로 다운받기-->

pip install -q -U google-generativeai

pip install mysql-connector-python

pip install python-dotenv

</br>

### .env 파일 세팅
.env 파일 생성
> .env 파일 유출 주의

```
GEMINI_API_KEY="gemini api 페이지에서 본인 api key 받아서 넣기"

DB_USER = 

DB_PASSWORD = 

DB_HOST=

DB_NAME=
```

<!-- 다운 받고 시작!! -->

### 예외처리 1

영화 시놉시스가 아래와 같은 내용을 담고 있으면 에러 발생함.

- HARM_CATEGORY_SEXUALLY_EXPLICIT: 성적으로 노골적인 콘텐츠
- HARM_CATEGORY_HATE_SPEECH: 증오 발언
- HARM_CATEGORY_HARASSMENT: 괴롭힘
- HARM_CATEGORY_DANGEROUS_CONTENT: 위험한 콘텐츠


### 예외처리 2

단기간에 api를 많이 호출하면, api 사용량을 초과해 다음과 같은 에러가 발생함.

- RESOURCE_TEMPORARILY_EXHAUSTED
- Too many requests in a short amount of time.

