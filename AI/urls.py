from django.urls import path
from AI.views import AIAssistantView, UserAIPlanListView

urlpatterns = [
    path('assistant/', AIAssistantView.as_view(), name='ai-assistant'),
    path('plans/', UserAIPlanListView.as_view(), name='user-ai-plans'),
]