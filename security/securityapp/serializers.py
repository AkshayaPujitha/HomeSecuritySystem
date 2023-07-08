from .models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class VerifyOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate_otp_code(self, value):
        crct_code = self.context['request'].session.get('crct_otp_code')
        if value != crct_code:
            raise serializers.ValidationError('Invalid OTP code')
        return value