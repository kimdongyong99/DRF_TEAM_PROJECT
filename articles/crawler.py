import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views import View
from rest_framework.response import Response


class Crawler(View):
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
