from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', "first_name", "last_name", "birth_date",
                  "email", "phone", "date_joined", 'password']
        read_only_fields = ["id", "date_joined"]
        extra_kwargs = {
            "password": {
                "write_only": True, }
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["username", "password", "email", "password2"]

    def validate(self, data):
        if not (data.get("username") or data.get("email")):
            raise serializers.ValidationError("Нужно указать username or email")

        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        if len(data['password']) <8:
            raise serializers.ValidationError("Пароль должен быть не меньше 8 символов")

        if not any(i.isdigit() for i in data['password']):
            raise serializers.ValidationError("Пароль должен содержать хотя бы 1 цифру")

        return data

    def create(self, validated_data):

        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        validated_data.pop('password2', None)

        user = User.objects.create_user(**validated_data)
        return user
