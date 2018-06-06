from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.company.serializers import CompanySerializer,AssignCompanySerializer,CompanyDetailSerializer
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from app.company.models import Company
from app.lib.response import ApiResponse
from app.lib.common import RequestOverwrite
from app.users.serializers import ProfileSerializer

class CompanyApi(APIView):
	def post(self,request):
		try:
			company_data = CompanySerializer(data=request.data)
			if not(company_data.is_valid()):
				return ApiResponse().error(company_data.errors, 400)
			company_data.save()
			return ApiResponse().success("Company added successfully", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error", 500)

	def get(self,request,company_id=None):
		try:

			if(company_id):
				try:
					get_data = CompanySerializer(Company.objects.get(is_deleted=False, id=company_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid company id", 400)
			else:
				company_data = Company.objects.filter(is_deleted=False).order_by('-id')
				get_data = CompanySerializer(company_data, many=True)
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting the company details", 500)

	def put(self,request,company_id):
		try:
			get_data = Company.objects.get(pk=company_id)
			update_data = CompanySerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Company details updated Successfully", 200)
			else:
				return ApiResponse().error("Error while updating the company details", 400)	
		except:
			return ApiResponse().error("Error", 500)

	def delete(self,request,company_id):
		try:
			Company.objects.filter(pk=company_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)


class AssignCompanies(APIView):
	def post(self,request):
		try:
			company_data = AssignCompanySerializer(data=request.data)
			if not(company_data.is_valid()):
				return ApiResponse().error(company_data.errors, 400)
			company_data.save()
			return ApiResponse().success("Company and User added successfully", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error", 500)


	def get(self, request, user_id):
		try:
			user = ProfileSerializer(UserProfile.objects.get(user = user_id))
			return ApiResponse().success(user.data, 200)
		except Exception as err:
			print (err)
			return ApiResponse().error("Problem occurs while fetching data", 500)

class UpdatedCountCompany(APIView):

	def get(self,request):
		try:
			total = Company.objects.filter(is_deleted = False).count()
			company = Company.objects.filter(is_deleted = False).order_by('-updated_at')[0]
			data = {'total_company': total, 'updated_company': company.name}	
			return ApiResponse().success(data, 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while getting total count or updated company info", 500)


class GetCompanyByDomain(APIView):
	
	def post(self,request):
		try:
			company = Company.objects.filter(is_deleted = False, url = request.data.get('domain_name'))[0]
			company_data = CompanyDetailSerializer(company)
			return ApiResponse().success(company_data.data, 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("There is no company behalf of this domain", 400)
	
