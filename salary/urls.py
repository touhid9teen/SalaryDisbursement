from django.urls import path
from .views import SalaryCreateAndListView, SalaryDisbursementDetailView,SalaryStatusUpdateView

urlpatterns = [
    path('file/upload/', SalaryCreateAndListView.as_view(), name='salary_create'),
    path('beneficiary/all/', SalaryDisbursementDetailView.as_view(), name='salary_list'),
    path('beneficiary/status/<int:beneficiary_id>/', SalaryStatusUpdateView.as_view(), name='salary_beneficiary_status'),
]