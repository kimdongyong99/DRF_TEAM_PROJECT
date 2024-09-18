from django.urls import path
from . import views, crawler
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="articles"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/comment/", views.CommentListCreateView.as_view()),
    path("<int:pk>/comment/<int:comment_pk>", views.CommentUpdateDeleteView.as_view()),
    path("<int:article_pk>/likes/", views.ArticleLikeView.as_view()),
    path("<int:comment_pk>/comment/likes/", views.CommentLikeView.as_view()),
    path('crawl/', crawler.Crawler.as_view(), name='crawl_news'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
