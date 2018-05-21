from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.company.serializers import CompanySerializer
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from app.company.models import Company
from app.lib.response import ApiResponse

class CompanyApi(APIView):
	def post(self,request):
		try:
			company_data = CompanySerializer(data=request.data)
			if not(company_data.is_valid()):
				return ApiResponse().error(company_data.errors,400)
			company_data.save()
			return ApiResponse().success("Company added successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding company",400)

	def get(self,request,company_id=None):
		try:
			if(company_id):
				company_data = Company.objects.filter(is_deleted=False,pk=company_id)[0]
				get_data = CompanySerializer(company_data)
			else:
				company_data = Company.objects.filter(is_deleted=False)
				get_data = CompanySerializer(company_data,many=True)
			return ApiResponse().success(get_data.data,200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting the company details",500)

	def put(self,request,company_id):
		try:
			get_data = Company.objects.get(pk=company_id)
			update_data = CompanySerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Company details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.errors,400)	
		except:
			return ApiResponse().error("Error while updating the company details",500)

	def delete(self,request,company_id):
		try:
			Company.objects.filter(pk=company_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 400)


class CompanyTemplate(TemplateView):
	def get(self,request):
		return render(request,'company/add_company.html')





