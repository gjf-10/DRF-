from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


from day08.models import Teacher
from day08.tserializer import TeacherSerializer, TeacherDeSerializer


class TeacherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            obj = Teacher.objects.filter(pk=id).first()     # 对象模型

            obj_serializer = TeacherSerializer(obj).data
            return Response({
                "status": 200,
                "message": "查询单个老师成功",
                "result": obj_serializer,
            })
        else:
            obj_all = Teacher.objects.all()
            objs_serializer = TeacherSerializer(obj_all, many=True).data
            print(obj_all)
            return Response({
                "status": 200,
                "message": "查询所有老师信息成功",
                "result": objs_serializer
            })

    def post(self, request, *args, **kwargs):
        req_data = request.data
        print(req_data, "从前端获取的数据")
        # 简单验证数据的合法性
        if not isinstance(req_data, dict) or req_data == {}:
            return Response({
                "status": 400,
                "message": "参数有误",
            })

        # 使用序列化器完成数据的反序列化
        # 在数据进行反序列化时需要指定关键字 data
        serializer = TeacherDeSerializer(data=req_data)



        # 需要对反序列化的数据进行校验，通过is_valid()方法对传递过来的参数进行校验，合法则继续
        if serializer.is_valid():
            # 调用save()方法进行数据的保存，必须重写create()方法
            teacher_ser = serializer.save()
            print(teacher_ser)
            return Response({
                "status": 200,
                "message": "教师添加成功",
                "result": TeacherSerializer(teacher_ser).data
            })
        else:
            return Response({
                "status": 400,
                "message": "员工添加失败",
                # 保存失败的信息会包含在 .errors中
                "results": serializer.errors
            })

