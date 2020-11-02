from rest_framework import serializers

from app.models import Book, Press


class BookSerializer(serializers.Serializer):
    # 序列化想要在前端展示的字段
    book_name = serializers.CharField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # pic = serializers.ImageField()
    # press_name = serializers.SerializerMethodField()

    # 要序列化外键如何序列化没有对应的字段

    # def get_press_name(self):
    #     return self.press_name
    # 可以自定义字段
    # get_字段名处理自定义类型能处理成自己想要显示在前端的形式


class BookDeSerializer(serializers.Serializer):
    # 对要存数据库的字段进行校验，
    book_name = serializers.CharField(max_length=20, min_length=1)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # pic = serializers.ImageField()
    # publish = serializers.SerializerMethodField()
    # 可以定义钩子函数
    def validate(self, attrs):
        # attrs 是上面写的所有字段以OrderDict的形式存储
        # attrs.get('字段名') 获取字段并做限制，不符合条件的用raise 异常的形式抛出
        return attrs
    # 可以定义局部钩子函数对某个字段做限制 validate_字段名(self, value), 也是raise 异常处理不合理情况
    # 重写自己的create方法来存数据

    def create(self, data):
        return Book.objects.create(**data)


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "pic", "address")


class BookSerializer2(serializers.ModelSerializer):
    publish = PressSerializer()

    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "publish")


class BookDeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")

        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 2,
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },
            # 可以添加其他字段的验证
        }

    def validate(self, attrs):
        print(attrs)
        return attrs

    def validate_book_name(self, obj):
        print("book_name:", obj)
        return obj


class BookModelSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields的字段包含需要序列化和反序列化的所有字段
        fields = ("book_name", "price", "publish", "press_name", "authors", "pic")

        extra_kwargs = {
            "book_name": {
                "required": True,   # 必填字段
                "min_length": 2,    # 最小长度
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            },
            # 指定某个字段只参与反序列化
            "publish": {
                "write_only": True
            },

            "pass_name": {
                "read_only": True
            },
            "authors": {
                "write_only": True
            },

        }

    def validate(self, attrs):
        print(attrs)
        return attrs

    def validate_book_name(self, obj):
        return obj