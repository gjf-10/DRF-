from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework.views import APIView

from app.models import Book
from app.serializer import BookSerializer, BookDeSerializer, BookSerializer2, BookDeModelSerializer, BookModelSerializer3


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # 获取路径中的参数
        id = kwargs.get('id')
        # 如果有该id 做查询
        if id:
            book_info = Book.objects.get(pk=id)
            # 将查询结果序列化返回到前端
            # serilizer = BookSerializer(book_info).data
            serilizer = BookModelSerializer3(book_info).data
            return Response({
                "status": 200,
                "message": "查询单本书成功",
                "result": serilizer
            })
        else:
            # 如果没有id 说明是查询全部
            book_all = Book.objects.all()
            # serilizer = BookSerializer(book_all, many=True).data
            serilizer = BookModelSerializer3(book_all, many=True).data
            print(serilizer)
            return Response({
                "status": 200,
                "message": "查询成功",
                "result": serilizer
            })

    def post(self, request, *args, **kwargs):
        # 获取post请求中的参数
        request_data = request.data
        # 做参数检验，格式和是否为空
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 400,
                "message": "添加失败",
                "result": "参数有误"
            })
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 400,
                "message": "参数格式有误",
            })
        # 如果参数没问题，需要序列化，参数检验，存数据
        serializer = BookDeSerializer(data=request_data, many=many)
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            "status": 200,
            "message": "修改成功",
            "result": BookSerializer(book_obj, many=many).data
        })
        # serializer.is_vailed()


class BookAPIView2(APIView):
    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            book = Book.objects.get(pk=book_id, is_delete=False)
            # data = BookSerializer2(book).data
            data = BookModelSerializer3(book).data
            return Response({
                "status": 200,
                "message": "查询单本图书成功",
                "result": data
            })
        else:
            book_all = Book.objects.all()
            # data = BookSerializer2(book_all, many=True).data
            data = BookModelSerializer3(book_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询所有图书成功",
                "results": data
            })

    def post(self, request, *args, **kwargs):
        """
        添加单个：参数格式是字典
        添加多个：参数格式列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.data

        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 400,
                "message": "参数格式有误",
            })

        # serializer = BookDeModelSerializer(data=request_data, many=many)
        serializer = BookModelSerializer3(data=request_data, many=many)
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()

        return Response({
            "status": 200,
            "message": "添加成功",
            # "results": BookSerializer2(book_obj, many=many).data
            "results": BookModelSerializer3(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个 删除多个
        单个删除：通过url传递单个删除的id
        多个删除：用 id {'ids':[1, 2, 3]}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        book_id = kwargs.get("id")

        if book_id:
            # 删除单个
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        print(response)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })

        return Response({
            "status": 400,
            "message": "删除失败或图书不存在"
        })

    def put(self, request, *args, **kwargs):
        """
        修改单个的全部字段，修改对象时，在调用序列化器检测数据时必须指定instance关键字
        在调用serializer.save() 底层是同过ModelSerializer内部的update()方法来完成更新
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # 获取要修改的对象的值
        request_data = request.data
        # 获取要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "图书不存在"
            })

        # 更新时需要对前端数据进行校验，及序列化器校验
        # 修改需要指定instance参数

        serializer = BookDeModelSerializer(data=request_data, instance=book_obj)
        serializer.is_valid()

        book = serializer.save()

        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookSerializer2(book).data
        })

    def patch(self, request, *args, **kwargs):
        """
        修改一个对象的部分字段
        使用序列化器修改对象时，必须指定instance关键字，
        在调用serializer.sava() 底层通过ModelSerializer的update()方法来完成的更新
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # 获取要修改的对象的值
        request_data = request.data
        # 需要获取要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "图书不存在"
            })
        # serializer = BookDeModelSerializer(data=request_data, instance=book_obj, partial=True)
        serializer = BookModelSerializer3(data=request_data, instance=book_obj, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookSerializer2(book_obj).data
        })


class BookGenericAPIView(GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin):
    queryset = Book.objects

    serializer_class = BookModelSerializer3

    lookup_field = "id"

    # 继承了get_queryset(), get_object(), get_serializer(),lookup_field()

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    # 这里的删除会真的从数据库中删除数据不是讲is_delete字段设置为True
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BookGenericAPIViewV3(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer3
    lookup_field = "id"


class BookViewSetView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer3

    def user_login(self, request, *args, **kwargs):
        # 可以在此完成登录的逻辑
        request_data = request.data
        print("登录成功")
        return Response("登录成功")

    def get_user_count(self, request, *args, **kwargs):
        # 完成获取用户数量的逻辑
        print("查询成功")
        return self.list(request, *args, **kwargs)