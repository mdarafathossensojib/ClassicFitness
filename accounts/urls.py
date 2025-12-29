from django.urls import path
from accounts.views import UserProfileView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
]