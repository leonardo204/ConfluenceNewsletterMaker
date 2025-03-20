# 뉴스레터 생성기

다양한 소스(Confluence, 웹)에서 정보를 수집하여 카테고리별 뉴스레터를 쉽게 생성할 수 있는 웹 애플리케이션입니다.

## 주요 기능

### 1. 다중 카테고리 지원
- **News**: 최신 소식 및 공지사항
- **Knowledge**: 지식 공유 및 참고 자료
- **Guide**: 가이드 및 튜토리얼

### 2. 다양한 소스 지원
- **Confluence**: Confluence 페이지 ID 기반 정보 수집
  - TL;DR 내용 자동 감지 및 요약 제공
  - 바로가기 링크 생성
- **Web**: URL 기반 웹 페이지 정보 스크래핑
  - 페이지 제목 및 설명 추출
  - 날짜 형식 [YY. MM. DD] 자동 추가

### 3. 복사 기능
- **항목별 복사**: 각 항목을 HTML 포맷(서식 유지)으로 복사
- **전체 복사**: 카테고리별로 정리된 전체 뉴스레터 복사
- **Confluence/Outlook 호환**: 복사된 내용을 Confluence나 Outlook에 붙여넣을 때 서식과 링크 유지

## 기술 스택

- **백엔드**: Flask (Python)
- **외부 라이브러리**:
  - Atlassian Python API (Confluence 연동)
  - BeautifulSoup4 (HTML 파싱)
  - Requests (웹 페이지 요청)
  - python-dotenv (환경 변수 관리)
- **프론트엔드**: HTML, CSS, JavaScript

## 설치 및 실행 방법

1. 저장소 클론
```bash
git clone [repository_url]
cd newsletter-generator
```

2. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용 추가:
```
CONFLUENCE_URL=https://your-confluence-instance.atlassian.net
CONFLUENCE_USERNAME=your_email@example.com
CONFLUENCE_API_TOKEN=your_api_token
```

4. 애플리케이션 실행
```bash
python app.py
```

5. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 사용 방법

1. 카테고리별 항목 입력
   - 항목 유형(Web/Confluence) 선택
   - URL 또는 Confluence 페이지 ID 입력
   - "+" 버튼으로 항목 추가

2. "생성하기" 버튼 클릭

3. 결과 확인 및 복사
   - 개별 항목 복사: "항목 복사" 버튼 클릭
   - 전체 뉴스레터 복사: "전체 내용 복사" 버튼 클릭

4. Confluence 또는 이메일에 붙여넣기

## 최근 업데이트

- 카테고리별 항목 입력 기능 추가
- Web/Confluence 구분 기능 추가
- Web 스크래핑 기능 구현
- HTML 포맷 유지 복사 기능 개선
- 브라우저 호환성 향상

## 참고 사항

- Confluence API 토큰은 Atlassian 계정에서 생성해야 합니다.
- Web 스크래핑 기능은 웹사이트의 구조에 따라 결과가 달라질 수 있습니다.
- 일부 웹사이트는 스크래핑을 제한할 수 있으니 이용 약관을 확인하세요.