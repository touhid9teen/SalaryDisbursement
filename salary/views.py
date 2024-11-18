from django.core.serializers import serialize
from requests import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from salary.models import SalaryBeneficiary, SalaryDisbursement
from salary.serializers import SalarySerializer
from users.authenticate import CustomAuthentication
from rest_framework.response import Response
from rest_framework import status

from users.models import Users
from users.permissions import IsManager, IsAdmin
from .tasks import update_Salary_Disbursement
import json
import os
from django.conf import settings
from pathlib import Path


class SalaryCreateAndListView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsManager]
    def post(self, request):
        salary_serializer = SalarySerializer(data=request.data)
        if salary_serializer.is_valid():
            salary_serializer.save()
            print("salary saved")
            try:
                file_record = salary_serializer.data['filepath']
                print('file_record = ', file_record)
                file_path = Path(settings.BASE_DIR) / file_record.lstrip('/')
                print('file_path = ', file_path)

                if not os.path.exists(file_path):
                    return Response({"error": f"File does not exist at {file_path}"}, status=status.HTTP_400_BAD_REQUEST)

                with open(file_path, 'r', encoding='utf-8') as file_:
                    content = file_.read().strip()
                    content_json = json.loads(content)
                    print("content_json = ", content_json)
                    update_Salary_Disbursement.delay(content_json)
            except json.JSONDecodeError as e:
                return Response(f"Error decoding JSON: {e}")
            except Exception as e:
                print('errr = ', repr(e))
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(salary_serializer.data, status=status.HTTP_201_CREATED)
        return Response(salary_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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