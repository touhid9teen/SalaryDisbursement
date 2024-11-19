from django.urls import path
from .views import SalaryCreateAndListView, SalaryDisbursementDetailView, SalaryStatusUpdateView, AllSalaryDisbursementView, SalaryDisbursementStatusUpdateView

urlpatterns = [
    path('file/upload/', SalaryCreateAndListView.as_view(), name='salary_create'),
    path('beneficiary/all/', SalaryDisbursementDetailView.as_view(), name='salary_list'),
    path('beneficiary/status/<int:beneficiary_id>/', SalaryStatusUpdateView.as_view(), name='salary_beneficiary_status'),
    path('disbursement/', AllSalaryDisbursementView.as_view(), name='salary_disbursement'),
    path('disbursement/status/<int:salary_id>/', SalaryDisbursementStatusUpdateView.as_view(), name='salary_disbursement_status'),
]