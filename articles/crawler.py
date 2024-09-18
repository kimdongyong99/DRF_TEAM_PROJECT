from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import JsonResponse
from django.views import View
from bs4 import BeautifulSoup
from Big_News.config_key import OPENAI_API_KEY
from openai import OpenAI

service = Service(executable_path="/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=service)
"""
CrawlerNews 는 네이버 야구 추천 뉴스를 제목과 url 을 클로링하고 
하이퍼 링크로 묶어 주는 api 를 제공합니다
(예시로 야구 를 가져왔지만 우리가 어떤 뉴스 페이지 를 만드냐에 따라
알맞는 뉴스를 크로링 해서 넣어주면 프론트 단 에서 필요한 곳에 사용할 수 있습니다) 
"""


class CrawlerNews(View):
    def get(self, request, *args, **kwargs):
        url = "https://sports.news.naver.com/kbaseball/index/"
        response = requests.get(url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list1 = soup.find("ul", class_="home_news_list")
        news_list2 = soup.find("ul", class_="division")

        news_info = ""
        if news_list1:
            for item in news_list1.find_all("li"):
                title_tag = item.find("a")
                if title_tag:
                    href = title_tag.get("href")
                    title = title_tag.get("title", "No title")
                    news_info += f'<a href="{href}">{title}</a><br>'
        if news_list2:
            for item in news_list2.find_all("li"):
                title_tag = item.find("a")
                if title_tag:
                    href = title_tag.get("href")
                    title = title_tag.get("title", "No title")
                    news_info += f'<a href="{href}">{title}</a><br>'
        # 팀원들에게 코드 리뷰 떄 필요한 코드
        # for link in soup.find_all('a'):
        #     href = link.get('href')
        #     title = link.get('title')
        #     news_info += f"href: {href}, title: {title}\n"

        return HttpResponse(f"크롤링 시작:<br>{news_info}")


"""
크로링한 기사를 요약하여 제공하는 API
"""
client = OpenAI(
    api_key=OPENAI_API_KEY,
)


class ArticleSummarizer(View):
    def get(self, request, *args, **kwargs):
        url = request.GET.get("url")

        if not url:
            return JsonResponse({"error": "URL이 제공되지 않았습니다."}, status=400)

        try:
            # Selenium 설정
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않도록 설정
            service = Service("/path/to/chromedriver")  # chromedriver 경로
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)

            # 페이지가 완전히 로드될 때까지 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "NewsEndMain_comp_article_content__PZYoE")
                )
            )

            html_content = driver.page_source
            driver.quit()

            # BeautifulSoup으로 콘텐츠 파싱
            soup = BeautifulSoup(html_content, "html.parser")
            content = self.extract_main_content(soup)

            if not content:
                return JsonResponse({"error": "기사를 찾을 수 없습니다."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        try:
            summary = self.summarize_content(content)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"summary": summary})

    def extract_main_content(self, soup):
        article_div = soup.find(
            "article", class_="NewsEndMain_comp_news_article__wMpnW _article_body"
        )
        content_div = (
            article_div.find("div", class_="_article_content") if article_div else None
        )

        if content_div:
            text = content_div.get_text(strip=True)
            if len(text) > 200:
                return text

        return None

    def summarize_content(self, content):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "사용자가 입력한 기사내용을 요약해서 알려주면돼",
                    },
                    {
                        "role": "user",
                        "content": f"{content}",
                    },
                ],
            )
            summary = completion.choices[0].message["content"].strip()
        except Exception as e:
            summary = f"요약 생성 중 오류가 발생했습니다: {str(e)}"
        return summary
