from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="articles"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/comment/", views.CommentListCreateView.as_view()),
    path("<int:pk>/comment/<int:comment_pk>", views.CommentUpdateDeleteView.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
