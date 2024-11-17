from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, EmailValidator
from rest_framework import serializers
from users.models import Users
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    conform_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = Users
        fields = ['email', 'contract_number', 'first_name', 'last_name', 'user_type', 'password', 'conform_password', 'gender', 'date_of_birth', 'company_id', 'address']
        extra_kwargs = {
            'email': {'required': True},
            'contract_number': {'required': True}
        }

    # def validate(self, attrs):


    def validate_email(self, email):
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already registered')
        validate_email(email)
        return email

    def validate_contract_number(self, contract_number):
        contract_number = contract_number.strip()

        if contract_number.startswith('+'):
            contract_number = contract_number[3:]
        if len(contract_number) == 13:
            contract_number = contract_number[2:]

        if not contract_number.isdigit() or len(contract_number) != 11:
            raise serializers.ValidationError(
                'Contract number must contain 11 digits (e.g., 01XXXXXXXXX).'
            )

        if Users.objects.filter(contract_number=contract_number).exists():
            raise serializers.ValidationError('Contract number is already registered.')

        return contract_number

    def validate(self, attrs):
        password = attrs.get('password')
        conform_password = attrs.get('conform_password')
        if password != conform_password:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs


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
            auth_kwargs = {'phone': email_or_phone, 'password': password}

        user = authenticate(**auth_kwargs)
        print("user", user, auth_kwargs)
        if user is None:
            raise serializers.ValidationError(_("Invalid email/phone or password."))

        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'contract_number', 'first_name', 'last_name', 'user_type', 'gender', 'date_of_birth', 'company_id', 'address']


