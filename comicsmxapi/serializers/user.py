from rest_framework import serializers
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Usuario inactivo.")
            else:
                raise serializers.ValidationError("Correo electrónico o contraseña incorrectos.")
        else:
            raise serializers.ValidationError("Se requiere un correo electrónico y una contraseña.")

        attrs['user'] = user
        return attrs