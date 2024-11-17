from django.contrib import admin
from salary.models import SalaryBeneficiary, SalaryDisbursement

# Register your models here.
admin.site.register(SalaryBeneficiary)
admin.site.register(SalaryDisbursement)