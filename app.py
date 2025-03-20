from flask import Flask, request, render_template
from atlassian import Confluence
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime

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
        summaries = []
        
        # 모든 카테고리 항목과 유형 가져오기
        categories = ["news", "knowledge", "guide"]
        
        for category in categories:
            items = request.form.getlist(f'{category}_items')
            types = request.form.getlist(f'{category}_types')
            
            # 각 항목에 맞는 유형이 있는지 확인
            while len(types) < len(items):
                types.append("Confluence")  # 기본 유형
            
            for i, (item, item_type) in enumerate(zip(items, types)):
                if not item.strip():
                    continue  # 빈 항목 건너뛰기
                
                if item_type == "Web":
                    try:
                        url = item.strip()
                        response = requests.get(url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        })
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # 웹 페이지에서 제목 가져오기
                        title_tag = soup.find('title')
                        title = title_tag.get_text() if title_tag else "제목 없음"
                        
                        # 날짜 형식 지정 [YY. MM. DD]
                        date_str = datetime.now().strftime('%y. %m. %d')
                        
                        # 제목에 날짜 추가
                        title = f"{title} [{date_str}]"
                        
                        # 요약 - 메타 설명 찾거나 첫 단락 사용
                        description_meta = soup.find('meta', attrs={'name': 'description'})
                        if description_meta and description_meta.get('content'):
                            summary = description_meta['content']
                        else:
                            # 첫 단락 또는 다른 콘텐츠 가져오기
                            paragraphs = soup.find_all('p')
                            content_text = ""
                            for p in paragraphs:
                                text = p.get_text(strip=True)
                                if len(text) > 50:  # 의미 있는 내용이 있는 단락만 사용
                                    content_text = text
                                    break
                            
                            summary = content_text[:200] + "..." if len(content_text) > 200 else content_text
                            if not summary:
                                summary = "내용 없음"
                        
                        link = url
                        
                    except Exception as e:
                        print(f"웹 페이지 처리 에러: {str(e)}")
                        title = f"웹 페이지 처리 오류 [{date_str}]"
                        summary = f"처리 실패: {str(e)}"
                        link = url
                    
                    summaries.append({
                        'category': category.capitalize(),
                        'title': title,
                        'summary': summary,
                        'link': link
                    })
                else:  # Confluence 유형
                    try:
                        page_id = item.strip()
                        print(f"페이지 ID 요청: {page_id}")
                        content = confluence.get_page_by_id(page_id, expand="body.storage")
                        print(f"페이지 제목: {content.get('title')}")
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
                            'category': category.capitalize(),
                            'title': title,
                            'summary': summary,
                            'link': link
                        })
                    except Exception as e:
                        print(f"에러 발생: {str(e)}")
                        summaries.append({
                            'category': category.capitalize(),
                            'title': "오류 발생",
                            'summary': f"처리 실패: {str(e)}",
                            'link': f"{os.environ['CONFLUENCE_URL']}/spaces/AMAICT/pages/{page_id}"
                        })

        return render_template('result.html', summaries=summaries)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)