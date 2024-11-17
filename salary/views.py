from requests import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from salary.models import SalaryBeneficiary
from salary.serializers import SalarySerializer
from users.authenticate import CustomAuthentication
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsManager, IsAdmin


class SalaryCreateAndListView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsManager]
    def post(self, request):
        salary = SalarySerializer(data=request.data)
        if salary.is_valid():
            salary.save()
            return Response(salary.data, status=status.HTTP_201_CREATED)
        return Response(salary.errors, status=status.HTTP_400_BAD_REQUEST)


class SalaryDisbursementDetailView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAdmin]
    def get(self, request):
        try:
            salary_bene = SalaryBeneficiary.objects.all()
            pageinator = PageNumberPagination()
            pageinator.page_size = 2
            pageinatorquery = pageinator.paginate_queryset(salary_bene, request)
            serializer = SalarySerializer(pageinatorquery, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return pageinator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SalaryStatusUpdateView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAdmin]
    def get(self, request, beneficiary_id):
        try:
            salary_bene = SalaryBeneficiary.objects.get(id=beneficiary_id)
            serializer = SalarySerializer(salary_bene)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, beneficiary_id):
        salary_beni = SalaryBeneficiary.objects.get(id=beneficiary_id)
        serializer = SalarySerializer(salary_beni,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)