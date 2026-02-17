from django.urls import path
from accounts.views import UserProfileView, UserDashboardAPIView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path("dashboard/", UserDashboardAPIView.as_view(), name="user-dashboard"),

]