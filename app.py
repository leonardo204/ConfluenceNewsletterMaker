from flask import Flask, request, render_template
from atlassian import Confluence
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

load_dotenv()

confluence = Confluence(
    url=os.environ["CONFLUENCE_URL"],
    username=os.environ["CONFLUENCE_USERNAME"],
    password=os.environ["CONFLUENCE_API_TOKEN"],
    api_version="cloud"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw_page_ids = request.form['page_ids']
        page_ids = [pid.strip() for pid in raw_page_ids.split('\n') if pid.strip()]
        summaries = []

        for page_id in page_ids:
            try:
                print(f"페이지 ID 요청: {page_id}")  # 디버깅 출력
                content = confluence.get_page_by_id(page_id, expand="body.storage")
                print(f"페이지 제목: {content.get('title')}")  # 디버깅 출력
                title = content.get("title", "제목 없음")
                body_html = content.get("body", {}).get("storage", {}).get("value", "내용 없음")

                soup = BeautifulSoup(body_html, 'html.parser')

                tldr = None
                elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                for i, element in enumerate(elements):
                    text = element.get_text(strip=True).lower()
                    if 'tl;dr' in text:
                        if i + 1 < len(elements):
                            tldr = elements[i + 1].get_text(strip=True)
                        else:
                            tldr = "TL;DR 내용이 없습니다."
                        break

                if tldr:
                    summary = tldr
                else:
                    body_text = soup.get_text(strip=True)
                    summary = body_text[:200] + "..." if len(body_text) > 200 else body_text

                link = f"{os.environ['CONFLUENCE_URL']}/spaces/AMAICT/pages/{page_id}"

                summaries.append({
                    'title': title,
                    'summary': summary,
                    'link': link
                })
            except Exception as e:
                print(f"에러 발생: {str(e)}")  # 디버깅 출력
                summaries.append({
                    'title': "오류 발생",
                    'summary': f"처리 실패: {str(e)}",
                    'link': f"{os.environ['CONFLUENCE_URL']}/spaces/AMAICT/pages/{page_id}"
                })

        return render_template('result.html', summaries=summaries)
    return render_template('index.html')

if name == 'main':
    app.run(debug=True, host='0.0.0.0', port=5000)
