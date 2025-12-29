from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

# Create your views here.

@api_view()
def api_root_view(request):
    return redirect('api-root')