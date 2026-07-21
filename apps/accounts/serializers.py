from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match."
                }
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user
    
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer used to return user information.
    Never expose passwords.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        refresh_token = self.validated_data["refresh"]

        token = RefreshToken(refresh_token)
        token.blacklist()

from django.contrib.auth.password_validation import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        # Check old password
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({
                "old_password": "Old password is incorrect."
            })

        # Check new passwords match
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        # Validate password strength
        validate_password(attrs["new_password"], user)

        return attrs

    def save(self):
        user = self.context["request"].user

        user.set_password(self.validated_data["new_password"])
        user.save()

        return user