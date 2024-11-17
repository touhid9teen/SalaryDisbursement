from requests import Response
from rest_framework.views import APIView

from salary.models import SalaryDisbursement
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
            salary = SalaryDisbursement.objects.all()
            serializer = SalarySerializer(salary, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
