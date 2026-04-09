from google import genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from AI.models import AIPlan
from decouple import config
import json
import os

api_key = os.environ.get('API_KEY') or config('API_KEY')
client = genai.Client(api_key=api_key)

class AIAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        plan_type = request.data.get('type', 'workout') 
        user_input = request.data.get('input', {})

        if not user_input:
            return Response({'error': 'Input data is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        input_text = json.dumps(user_input)
        # AI Prompt Engineering
        prompt = f"Expert fitness advice for {plan_type} based on: {input_text}. Short bullet points only."
        
        try:
            response = client.models.generate_content(
                model='gemini-3-flash-preview', 
                contents=prompt
            )

            if response and response.text:
                ai_text = response.text
                
                # Save to Database
                AIPlan.objects.create(
                    user=user,
                    plan_type=plan_type,
                    input_data=user_input,
                    ai_response=ai_text
                )
                return Response({'response': ai_text}, status=status.HTTP_200_OK)
            
            return Response({'error': 'AI generated an empty response.'}, status=500)
            
        except Exception as e:
            print(f"DEBUG: Error calling Gemini API -> {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAIPlanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = AIPlan.objects.filter(user=request.user).order_by('-created_at')
        data = [{
            "id": p.id,
            "type": p.plan_type,
            "response": p.ai_response,
            "date": p.created_at.strftime("%d %b, %Y")
        } for p in plans]
        return Response(data)