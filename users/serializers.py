from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "name", "role"]
        extra_kwargs = {'password': {'write_only': True}}

    # Override the save method to hash the user password
    def save(self, **kwargs):
        password = self.validated_data.get('password')
        if password:
            self.validated_data['password'] = self.instance.set_password(password) if self.instance else User().set_password(password)
        
        return super().save(**kwargs)


  

