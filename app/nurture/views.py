from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.nurture.serializers import NurtureSerializer,NurtureUrlSerializer
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from app.nurture.models import Nurture,NurtureUrl
from app.lib.response import ApiResponse
from app.lib.common import AccessUserObj, RequestOverwrite
from app.users.models import UserProfile

class NurtureApi(APIView):
	def post(self,request):
		try:
			# user = AccessUserObj().fromToken(request).user
			# user_id = UserProfile.objects.get(user_id = user.id)
			# print(user.id)
			# if (user_id.role.id == 3) or (user_id.role.id == 1):
			nurture_data = NurtureSerializer(data = request.data)
			if not(nurture_data.is_valid()):
				return ApiResponse().error(nurture_data.errors,400)
			nurture_data.save()
			if(request.data.get('url_name')):
				nurture = Nurture.objects.get(id = nurture_data.data.get('id'))
				NurtureUrl.objects.create(nurture = nurture, name = request.data.get('url_name') ,url = request.data.get('url'))
			return ApiResponse().success("Nurture added successfully", 200)
			# return ApiResponse().error("You are not authorised to create nurture", 400)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding nurture", 500)

	def get(self,request,nurture_id=None):
		try:
			if(nurture_id):
				nurture_data = Nurture.objects.filter(is_deleted=False,pk=nurture_id)[0]
				get_data = NurtureSerializer(nurture_data)
			else:
				nurture_data = Nurture.objects.filter(is_deleted=False)
				get_data = NurtureSerializer(nurture_data, many=True)
				print(get_data.data)
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Nurture does not exists", 400)

	def put(self,request,nurture_id):
		try:
			get_data = Nurture.objects.get(pk=nurture_id)
			print(get_data.company.id)
			RequestOverwrite().overWriteUserId(request, {'company':get_data.company.id})

			print(request.data)
			update_data = NurtureSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Nurture details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.errors, 400)	
		except Exception as err:
			print(err)
			return ApiResponse().error("Error", 500)

	def delete(self,request,nurture_id):
		try:
			Nurture.objects.filter(pk=nurture_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)

class NurtureDataByCompanyId(APIView):
	def get(self,request,company_id=None):
		try:
			if(company_id):
				try:
					nurture_data = Nurture.objects.filter(is_deleted=False, company_id=company_id)
					get_data = NurtureSerializer(nurture_data, many=True)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide company id", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Nurture matching query does not exist", 500)

class NurtureUrlApi(APIView):
	def post(self,request):
		try:
			nurture_data = NurtureUrlSerializer(data=request.data)
			if not(nurture_data.is_valid()):
				return ApiResponse().error(nurture_data.errors, 400)
			nurture_data.save()
			return ApiResponse().success("Nurtureurl added successfully", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding Nurtureurl", 500)

	def get(self,request,nurtureurl_id=None):
		try:
			if(nurtureurl_id):
				nurture_data = NurtureUrl.objects.filter(is_deleted=False,pk=nurtureurl_id)[0]
				get_data = NurtureUrlSerializer(nurture_data)
			else:
				nurture_data = NurtureUrl.objects.filter(is_deleted=False)
				get_data = NurtureUrlSerializer(nurture_data,many=True)
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting nurture url", 500)

	def put(self,request,nurtureurl_id):
		try:
			get_data = NurtureUrl.objects.get(pk=nurtureurl_id)
			update_data = NurtureUrlSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Nurtureurl details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.data, 400)	
		except:
			return ApiResponse().error("Error", 500)

	def delete(self,request,nurtureurl_id):
		try:
			NurtureUrl.objects.filter(pk=nurtureurl_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)


class UrlByNurture(APIView):
	def get(self,request,nurture_id=None):
		try:
			if(nurture_id):
				try:
					nurtureurl_data = NurtureUrl.objects.filter(is_deleted=False, nurture_id=nurture_id)
					get_data = NurtureUrlSerializer(nurtureurl_data, many=True)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide nurture id", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("NurtureUrl matching query does not exist", 500)