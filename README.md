# Confluence 뉴스레터 생성기

Confluence 페이지 ID를 입력하면 해당 페이지의 내용을 요약하여 뉴스레터 형식으로 생성해주는 웹 애플리케이션입니다.

## 기능 설명

- Confluence 페이지 ID 여러 개를 입력받아 각 페이지의 내용을 처리
- 페이지 내에 'TL;DR' 섹션이 있으면 해당 내용을 요약으로 사용
- 'TL;DR' 섹션이 없으면 페이지 첫 200자를 요약으로 사용
- 각 페이지의 제목, 요약 내용, 원본 페이지 링크를 포함한 뉴스레터 생성
- 생성된 뉴스레터는 Outlook 이메일에 복사하여 사용 가능

## 설치 방법

1. Python 3.9 이상 설치
   - 이 프로젝트는 Python 3.9 이상의 버전이 필요합니다.
   - [Python 다운로드 페이지](https://www.python.org/downloads/)

2. 저장소 클론 또는 다운로드
   ```
   git clone [저장소 URL]
   cd [프로젝트 폴더]
   ```

3. 가상 환경 생성 및 활성화 (선택사항)
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. 필요한 패키지 설치
   ```
   pip install -r requirements.txt
   ```

4. 환경 변수 설정
   - 프로젝트에 포함된 `.env.example` 파일을 `.env`로 복사
   ```
   cp .env.example .env  # Windows: copy .env.example .env
   ```
   - `.env` 파일을 열고 다음 변수를 자신의 환경에 맞게 수정:
     ```
     CONFLUENCE_URL=https://altimedia.atlassian.net/wiki
     CONFLUENCE_USERNAME=id@domain.com
     CONFLUENCE_API_TOKEN=<your-api-key>
     ```

## 디렉토리 구조

```
뉴스레터-생성기/
├── app.py              # 메인 애플리케이션 코드
├── requirements.txt    # 필요한 패키지 목록
├── .env.example        # 환경 변수 예시 파일
├── .env                # 실제 환경 변수 (생성 필요)
└── templates/
    ├── index.html      # 메인 페이지 템플릿
    └── result.html     # 결과 페이지 템플릿
```

## 사용 방법

1. 애플리케이션 실행
   ```
   python app.py
   ```

2. 웹 브라우저에서 접속
   - 로컬 접속: http://127.0.0.1:5000
   - 동일 네트워크 내 접속: http://[서버IP]:5000
   - 기본적으로 모든 네트워크 인터페이스(0.0.0.0)에서 요청을 수신합니다.

3. Confluence 페이지 ID 입력
   - 한 줄에 하나씩 Confluence 페이지 ID 입력
   - 예시:
     ```
     3840082544
     3840049779
     ```

4. "뉴스레터 생성" 버튼 클릭

5. 생성된 뉴스레터 내용을 복사하여 Outlook 또는 다른 메일 클라이언트에 붙여넣기

## 실행 모습
   - 뉴스레터 입력 화면
   
     <img width="961" alt="image" src="https://github.com/user-attachments/assets/cc5bf59d-1581-4212-aa1e-e103ce50f5c8" />
   
   - 생성된 뉴스 레터 화면

     <img width="629" alt="image" src="https://github.com/user-attachments/assets/940b7e73-aa3b-45f5-a056-cd3cd6638019" />


## Confluence API 토큰 생성 방법

1. Atlassian 계정으로 로그인
2. 프로필 > 계정 설정 > 보안 > API 토큰 생성
3. 토큰 이름 지정 후 토큰 생성
4. 생성된 토큰을 `.env` 파일의 `CONFLUENCE_API_TOKEN` 값으로 사용

## 문제 해결

- 페이지 ID가 올바르지 않은 경우 오류 메시지가 표시됩니다.
- 서버 실행 중 문제가 발생할 경우 콘솔 로그를 확인하세요.
- Confluence API 연결 문제가 있을 경우 환경 변수를 확인하세요.
- 네트워크 접속 문제가 있는 경우:
  - 방화벽 설정에서 5000 포트가 허용되어 있는지 확인하세요.
  - `0.0.0.0` 바인딩은 모든 네트워크 인터페이스에서 접속을 허용합니다.
