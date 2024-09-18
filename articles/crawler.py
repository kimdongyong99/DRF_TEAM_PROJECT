from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import JsonResponse, HttpResponse
from django.views import View
from bs4 import BeautifulSoup
from Big_News.config_key import OPENAI_API_KEY
import requests
import os
from selenium.webdriver.chrome.service import Service
from openai import OpenAI
from django.urls import reverse


class CrawlerNewsList(View):
    def get(self, request, *args, **kwargs):
        url = "https://sports.news.naver.com/kbaseball/index/"
        response = requests.get(url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        news_info = self.extract_news(soup, "ul", "home_news_list")
        news_info += self.extract_news(soup, "ul", "division")

        return HttpResponse(f"크롤링 시작:<br>{news_info}")

    def extract_news(self, soup, tag, class_name):
        news_list = soup.find(tag, class_=class_name)
        news_info = ""
        if news_list:
            for item in news_list.find_all("li"):
                title_tag = item.find("a")
                if title_tag:
                    href = title_tag.get("href")
                    title = title_tag.get("title", "No title")
                    news_info += f'<a href="{href}">{title}</a><br>'
        return news_info


client = OpenAI(api_key=OPENAI_API_KEY)


class WebDriverManager:
    def __enter__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=ChromeService(executable_path="/opt/homebrew/bin/chromedriver"),
            options=chrome_options,
        )
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()


class CrawlerNewsSummary(View):
    def get(self, request, *args, **kwargs):
        url = "https://sports.news.naver.com/kbaseball/index/"
        response = requests.get(url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        news_info = self.extract_news(soup, "ul", "home_news_list")
        news_info += self.extract_news(soup, "ul", "division")

        return HttpResponse(
            f"""
            크롤링 시작:<br>
            {news_info}
        """
        )

    def extract_news(self, soup, tag, class_name):
        news_list = soup.find(tag, class_=class_name)
        news_info = ""
        if news_list:
            for item in news_list.find_all("li"):
                title_tag = item.find("a")
                if title_tag:
                    href = title_tag.get("href")
                    title = title_tag.get("title", "No title")
                    news_info += (
                        f'<a href="{reverse("summarize")}?url={href}">{title}</a><br>'
                    )
        return news_info


class ArticleSummarizer(View):
    def get(self, request, *args, **kwargs):
        url = request.GET.get("url")

        if not url:
            return JsonResponse({"error": "URL이 제공되지 않았습니다."}, status=400)

        try:
            with WebDriverManager() as driver:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "NewsEndMain_comp_article_content__PZYoE")
                    )
                )
                html_content = driver.page_source
        except Exception as e:
            return JsonResponse(
                {"error": f"웹 크롤링 중 오류 발생: {str(e)}"}, status=500
            )

        soup = BeautifulSoup(html_content, "html.parser")
        content = self.extract_main_content(soup)

        if not content:
            return JsonResponse({"error": "기사를 찾을 수 없습니다."}, status=404)

        try:
            summary = self.summarize_content(content)
        except Exception as e:
            return JsonResponse(
                {"error": f"요약 생성 중 오류 발생: {str(e)}"}, status=500
            )

        return JsonResponse({"summary": summary})

    def extract_main_content(self, soup):
        article_div = soup.find(
            "article", class_="NewsEndMain_comp_news_article__wMpnW _article_body"
        )
        if article_div:
            content_div = article_div.find("div", class_="_article_content")
            if content_div:
                text = content_div.get_text(strip=True)
                if len(text) > 200:
                    return text
        return None

    def summarize_content(self, content):
        """추출한 기사를 요약하는 함수"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "이 기사를 간단히 요약해 주세요."},
                {"role": "user", "content": content},
            ],
        )
        return response.choices[0].message.content.strip()
