from django.urls import path
from company import views

urlpatterns = [
    path('list/', views.CompanyCreateAndListView.as_view(), name='company-create-and-list'),
    path('status/<int:company_id>',views.CompanyStatusAndUpdateView.as_view(), name='company-status-and-update'),
]