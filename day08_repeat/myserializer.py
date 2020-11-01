from rest_framework import serializers, exceptions

# 序列化需要写想要传给前端对应数据的字段
from day08_repeat.models import Book


class BookSerializer(serializers.Serializer):
    book_name = serializers.CharField()
    author = serializers.CharField()
    publish = serializers.CharField()
    # 可自定义前端显示格式
    price = serializers.SerializerMethodField()
    def get_price(self, obj):
        return '打折价%s' % (obj.price)


class BookDeSerializer(serializers.Serializer):
    # 反序列器，将前端数据转换为合适数据库存储的数据，并做一些验证
    book_name = serializers.CharField(max_length=50, min_length=2)
    author = serializers.CharField(max_length=50, min_length=0)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    publish = serializers.CharField(max_length=50, min_length=5)

    def validate(self, attrs):
        # 可以对上面写的这些字段进行校验
        book_name = attrs.get("book_name")
        if Book.objects.filter(book_name=book_name):
            raise exceptions.ValidationError("数据库中已有该本书，如果要修改该书信息请选择修改。")
        return attrs

    def validate_price(self, value):
        if value <= 0:
            raise exceptions.ValidationError("价格有问题")
        return value

    def create(self, data):
        # print(data)
        return Book.objects.create(**data)