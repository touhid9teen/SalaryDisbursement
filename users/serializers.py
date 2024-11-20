from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, EmailValidator
from rest_framework import serializers
from users.models import Users
from django.utils.translation import gettext_lazy as _


from django.core.validators import validate_email
from rest_framework import serializers
from .models import Users

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'email', 'contract_number', 'password',
            'conform_password', 'first_name', 'last_name',
            'user_type', 'gender', 'date_of_birth',
            'address', 'company_id'
        ]
        extra_kwargs = {
            'password': {'write_only' : True, 'required' : True },
            'conform_password': {'write_only' : True, 'required' : True }
        }

    def validate(self, attrs):
        # Validate email
        email = attrs.get('email')
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})
        try:
            validate_email(email)
        except Exception as e:
            raise serializers.ValidationError({'email': 'Invalid email address'})

        # Validate contract number
        contract_number = attrs.get('contract_number', '').strip()

        if contract_number.startswith('+'):
            contract_number = contract_number[3:]
        if len(contract_number) == 13:
            contract_number = contract_number[2:]

        if not contract_number.isdigit() or len(contract_number) != 11:
            raise serializers.ValidationError({
                'contract_number': 'Contract number must contain 11 digits (e.g., 01XXXXXXXXX).'
            })

        if Users.objects.filter(contract_number=contract_number).exists():
            raise serializers.ValidationError({'contract_number': 'Contract number is already registered.'})

        # Ensure contract_number back to original value for consistency
        attrs['contract_number'] = contract_number

        # Validate password
        password = attrs.get('password')
        conform_password = attrs.get('conform_password')
        if password != conform_password:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        return attrs

    def create(self, validated_data):
        validated_data.pop('conform_password')  # Remove conform_password before saving
        return Users.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_email_or_phone(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)
            self.context['is_email'] = True
        except ValidationError:
            if value.isdigit() and len(value) == 11:
                self.context['is_phone'] = True
            else:
                raise serializers.ValidationError(_("Enter a valid email or phone number."))

        return value

    def validate(self, data):
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')
        print("email or phone", email_or_phone, password)
        # Determine if identifier is email or phone
        auth_kwargs = {'username': email_or_phone, 'password': password}
        if self.context.get('is_phone'):
            auth_kwargs = {'username': email_or_phone, 'password': password}

        user = authenticate(**auth_kwargs)
        print("user", user, auth_kwargs)
        if user is None:
            raise serializers.ValidationError(_("Invalid email/phone or password."))

        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'contract_number', 'first_name', 'last_name', 'user_type', 'gender', 'date_of_birth', 'company_id', 'address']


