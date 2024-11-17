from requests import Response
from rest_framework.views import APIView
from salary.serializers import SalarySerializer
from users.authenticate import CustomAuthentication
from rest_framework.response import Response
from rest_framework import status


class SalaryCreateAndListView(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self, request):
        salary = SalarySerializer(data=request.data)
        if salary.is_valid():
            salary.save()
            return Response(salary.data, status=status.HTTP_201_CREATED)
        return Response(salary.errors, status=status.HTTP_400_BAD_REQUEST)