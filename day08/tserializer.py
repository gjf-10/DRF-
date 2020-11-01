from rest_framework.serializers import Serializer
from rest_framework import serializers

from day07 import settings
from day08.models import Teacher

# 前端给的A，经过反序列化变为a，在经过序列化变为A
# 前端获取的数据需要反序列化为Model对象存在数据库中，这时需要检查字段的合法性。
# 后端取出的数据需要序列化为json格式response给前端


class TeacherSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    course = serializers.CharField()
    # 自定义字段，序列化
    pic = serializers.SerializerMethodField()
    def get_pic(self,obj):
        return "%s%s%s" % ("http:127.0.0.1:8000/", settings.MEDIA_URL, str(obj.pic))
    # gender = serializers.IntegerField()
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj):
        print(obj.get_gender_display())
        return obj.get_gender_display()


# 反序列化
class TeacherDeSerializer(serializers.Serializer):
    # 提供需要反序列化的字段
    name = serializers.CharField(max_length=20, min_length=1)
    age = serializers.IntegerField()
    course = serializers.CharField(max_length=20, min_length=2)
    pic = serializers.ImageField(default='pic/1.jpg')
    gender = serializers.IntegerField()

    def create(self, data):
        print(self)
        print(data)
        return Teacher.objects.create(**data)