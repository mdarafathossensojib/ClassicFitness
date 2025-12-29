from django.urls import path, include
from api import views
from rest_framework_nested import routers
from classes.views import FitnessClassViewSet
from memberships.views import MembershipPlanViewSet


router = routers.DefaultRouter()
router.register('classes', FitnessClassViewSet, basename='fitness-class')
router.register('membership-plans', MembershipPlanViewSet, basename='membership-plans')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('accounts/', include('accounts.urls')),

]
