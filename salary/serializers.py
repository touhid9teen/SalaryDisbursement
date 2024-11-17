from rest_framework import serializers
from salary.models import SalaryBeneficiary


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryBeneficiary
        fields = '__all__'