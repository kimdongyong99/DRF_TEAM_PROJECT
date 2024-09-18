from django.urls import path
from django.conf import settings
from . import views
from .views import ArticleListView
from django.conf.urls.static import static
from .crawler import ArticleSummarizer, CrawlerNewsList, CrawlerNewsSummary


urlpatterns = [
    path("", views.ArticleListView.as_view(), name="articles"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/comment/", views.CommentListCreateView.as_view()),
    path("<int:pk>/comment/<int:comment_pk>", views.CommentUpdateDeleteView.as_view()),
    path("<int:article_pk>/likes/", views.ArticleLikeView.as_view()),
    path("<int:comment_pk>/comment/likes/", views.CommentLikeView.as_view()),
    path("newssummary/", CrawlerNewsSummary.as_view(), name="news_list"),
    path("news/", CrawlerNewsList.as_view(), name="news_list"),
    path("summarize/", ArticleSummarizer.as_view(), name="summarize"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
