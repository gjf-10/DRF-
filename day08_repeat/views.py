from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


from day08_repeat.models import Book
from day08_repeat.myserializer import BookSerializer, BookDeSerializer


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # 获取前端要查询书对饮的id
        id = kwargs.get('id')
        # 如果获取到了说明要查的单本书
        # try:


        # except:
        #     return Response({
        #         "status": 400,
        #         "message": "单本书查询成功",
        #         "result": "请检查传的参数，没找到对应的书籍"
        #     })
        if id:
            # 从数据库中找到对应的书的信息

            book_info = Book.objects.get(pk=id)
            # 这儿有个问题如果book_info 是一个空对象，那么，应该怎么处理
            # 1.book_info = Book.objects.filter(pk=id)[0] ,用自定义异常，返回的response不准确
            # 2.直接在book_info这儿判断如果为空就不进行序列化返回原因。

            # 获取到数据后要序列化后传给前端
            serializer = BookSerializer(book_info).data  # 序列化的是model对象
            return Response({
                "status": 200,
                "message": "单本书查询成功",
                "result": serializer
            })
        else:
            # 查询所有书，
            books = Book.objects.all()
            #　序列化books返回给前端
            # serializer = BookSerializer(books).data  # books 是一个QuerySet对象需要添加满意属性
            serializer = BookSerializer(books, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有书成功",
                "result": serializer,
            })

    # 请求添加数据
    def post(self, request, *args, **kwargs):
        req_data = request.data     # 获取要添加的数据

        # 进一步检测数据是否合法，如果是添加一条数据,判断是否为字典对象，是否为空
        if isinstance(req_data, dict) and req_data != {}:
            # 数据格式正确，且有内容，反序列化数据
            d_serializer = BookDeSerializer(data=req_data)
            print(d_serializer)
            if d_serializer.is_valid():
                book = d_serializer.save()
                return Response({
                    "status": 200,
                    "message": "添加数据成功",
                    "result": BookSerializer(book).data
                })
            else:
                return Response({
                    "status": 400,
                    "message": "添加数据失败",
                    "results": d_serializer.errors
                })
        else:
            return Response({
                "status": 200,
                "message": "数据参数不正确"
            })
