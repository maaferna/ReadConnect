from rest_framework import serializers

from .models import UserBookStatus, Book, UserProfile


class BookWithUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model


class UserBookStatusSerializer(serializers.ModelSerializer):
    book = BookWithUserStatusSerializer()  # Include Book fields in UserBookStatus serializer

    class Meta:
        model = UserBookStatus
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
