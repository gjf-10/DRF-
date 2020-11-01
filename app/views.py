from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User


def index(request, **kwargs):
    if request.method == "GET":
        print("这是get请求")
    else:
        print(request.method)
    return HttpResponse('OK')


class UserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")


class UserViewAPI(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        print(id,)
        try:
            user = User.objects.filter(id=id).first()
            return Response({
                "status": 200,
                "message": "查询成功",
                "result": {
                    "username": user.username,
                    "password": user.password,
                }
            })
        except:
            print('查找数据不存在')
            return Response({
                "status": 400,
                "message": "没有该数据",
                "result": None
            })

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get("password")
        print(username, password)
        try:
            User.objects.create(username=username, password=password)
            return Response({
                'status': 200,
                'message': "添加数据成功",
            })
        except:
            print("添加失败")
            return Response({
                'status': 500,
                'message': "可能是用户名或密码太长"
            })

