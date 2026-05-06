from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    full_name = serializers.CharField(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'first_name', 'last_name',
            'full_name', 'role', 'role_display', 'avatar',
            'date_of_birth', 'gender', 'address', 'city',
            'state', 'country', 'pincode', 'is_active',
            'is_verified', 'date_joined', 'last_login',
            'employee_id', 'salary', 'joining_date'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_verified']
        
class UserCreateSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone',
            'role', 'date_of_birth', 'gender',
            'address', 'city', 'state', 'country', 'pincode',
            'employee_id', 'salary', 'joining_date'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        if attrs.get('role') == 'worker' and not attrs.get('employee_id'):
            raise serializers.ValidationError(
                {'employee_id': 'Employee ID is required for workers.'}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details.
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone',
            'avatar', 'date_of_birth', 'gender',
            'address', 'city', 'state', 'country', 'pincode',
            'salary', 'designation'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password_confirm': 'Passwords do not match.'}
            )
        
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users (minimal fields).
    """
    full_name = serializers.CharField(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role',
            'role_display', 'phone', 'is_active',
            'employee_id', 'designation'
        ]
        
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )


class TokenResponseSerializer(serializers.Serializer):
    """
    Serializer for token response.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
