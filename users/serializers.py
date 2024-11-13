from django.core.validators import validate_email
from rest_framework import serializers
from users.models import Users


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
class Meta:
    model = Users
    fields = ['id', 'email', 'contract_number', 'user_type', 'password']
    extra_kwargs = {
        'email': {'write_only': True, 'required': True},
        'contract_number': {'write_only': True, 'required': True}
    }

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