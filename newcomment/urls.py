from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from authentication.views import LoginAPIView, SignupAPIView
from comments.views import AddRatingAPIView, CommentViewSet, PostViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'posts', PostViewSet, basename='post')


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path("user/signup/", SignupAPIView.as_view(), name="user-signup"),
    path("user/login/", LoginAPIView.as_view(), name="user-login"),
    path('comment/<int:comment_id>/add_rating/',
         AddRatingAPIView.as_view(), name='add_rating'),
]
