from django.urls import path, include
from rest_framework_nested import routers
from classes.views import FitnessClassViewSet
from memberships.views import MembershipPlanViewSet
from attendance.views import AttendanceViewSet
from services.views import GymServiceViewSet, GymGalleryViewSet
from feedback.views import ClassFeedbackViewSet, FeedbackViewSet


router = routers.DefaultRouter()
router.register('classes', FitnessClassViewSet, basename='fitness-class')
router.register('membership-plans', MembershipPlanViewSet, basename='membership-plans')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('services', GymServiceViewSet, basename='services')
router.register('gallery', GymGalleryViewSet, basename='gallery')
router.register('feedback', FeedbackViewSet, basename='feedback')

classes_router = routers.NestedSimpleRouter(router, 'classes', lookup='class')
classes_router.register('class-feedback', ClassFeedbackViewSet, basename='class-feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(classes_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('accounts/', include('accounts.urls')),
    path('reports/', include('reports.urls')),

]
