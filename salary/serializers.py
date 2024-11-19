from rest_framework import serializers
from salary.models import SalaryBeneficiary, SalaryDisbursement


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryBeneficiary
        fields = '__all__'


class SalaryDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryDisbursement
        fields = '__all__'