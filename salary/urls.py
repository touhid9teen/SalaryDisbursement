from django.urls import path
from .views import SalaryCreateAndListView

urlpatterns = [
    path('status/', SalaryCreateAndListView.as_view(), name='salary_create'),
]