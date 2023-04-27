from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, ListUsers, UserTokenView, UserViewSet, ScoreEditView, DartsPlayerAPIView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [

    path('api/token/', UserTokenView.as_view(), name='generate_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name="registration") ,
    path('home/',   ListUsers.as_view(), name="home" ),
    path('user/', UserViewSet.as_view(), name="users" ),
    path('edit/', ScoreEditView.as_view(), name='user-edit'),
    path('adduser/', DartsPlayerAPIView.as_view(), name="add-user" )

]
