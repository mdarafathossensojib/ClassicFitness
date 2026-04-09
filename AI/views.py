import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from AI.models import AIPlan
from decouple import config
import json

genai.configure(api_key='AIzaSyAKJoGNoHczfUE_qU68qo6_4vW5C2uKn1E')


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
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)

            if not response or not hasattr(response, 'text'):
                 return Response({'error': 'AI could not generate a response. Please try again.'}, status=500)
            
            ai_text = response.text
            
            # Save to Database
            AIPlan.objects.create(
                user=user,
                plan_type=plan_type,
                input_data=user_input,
                ai_response=ai_text
            )
            
            return Response({'response': ai_text}, status=status.HTTP_200_OK)
        except Exception as e:
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