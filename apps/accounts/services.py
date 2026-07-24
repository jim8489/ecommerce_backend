from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:

    @staticmethod
    def register(validated_data):
        password = validated_data.pop("password")

        return User.objects.create_user(
            password=password,
            **validated_data,
        )

    @staticmethod
    def update_profile(user, validated_data):
        for key, value in validated_data.items():
            setattr(user, key, value)

        user.save()

        return user