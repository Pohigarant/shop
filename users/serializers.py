from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', "first_name", "last_name", "birth_date",
                  "email","phone","date_joined", 'password']
        read_only_fields = ["id","date_joined"]
        extra_kwargs = {
            "password": {
                "write_only": True, }
        }