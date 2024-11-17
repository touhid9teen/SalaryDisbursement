from django.db import models

from company.models import Company
from users.models import Users


class SalaryBeneficiary(models.Model):
    uploader = models.ForeignKey(Users, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    filepath = models.FileField(upload_to='documents/salary')


class SalaryDisbursement(models.Model):
    employ = models.ForeignKey(Users, on_delete=models.CASCADE)
    wallet_no = models.IntegerField()
    amount = models.IntegerField()
    update = models.DateTimeField(auto_now_add=True)
    beneficiary_id = models.ForeignKey(SalaryBeneficiary, on_delete=models.CASCADE)