from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.roles.serializers import RoleSerializer
from app.lib.response import ApiResponse


class RoleView(APIView):
	
	def post(self,request):
		try:
			role_data = RoleSerializer(data=request.data)
			if not(role_data.is_valid()):
				return ApiResponse().error(role_data.errors,400)
			role_data.save()
			return ApiResponse().success("Role created successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while assign the role",500)


	

