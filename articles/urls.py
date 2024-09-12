from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="articles"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
