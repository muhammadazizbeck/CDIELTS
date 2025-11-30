from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class ArticleAPIView(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ArticleRetrieveAPIView(APIView):
    def get(self,request,pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
