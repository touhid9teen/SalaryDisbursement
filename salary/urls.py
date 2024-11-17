from django.urls import path
from .views import SalaryCreateAndListView

urlpatterns = [
    path('file/upload/', SalaryCreateAndListView.as_view(), name='salary_create'),
    path('beneficiary/all/', SalaryCreateAndListView.as_view(), name='salary_list'),
]