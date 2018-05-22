from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.nurture.serializers import NurtureSerializer,NurtureUrlSerializer
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from app.nurture.models import Nurture,NurtureUrl
from app.lib.response import ApiResponse

class NurtureApi(APIView):
	def post(self,request):
		print("dfjhg")
		try:
			nurture_data = NurtureSerializer(data=request.data)
			if not(nurture_data.is_valid()):
				return ApiResponse().error(nurture_data.errors,400)
			nurture_data.save()
			return ApiResponse().success("Nurture added successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding nurture",400)

	def get(self,request,nurture_id=None):
		try:
			if(nurture_id):
				nurture_data = Nurture.objects.filter(is_deleted=True,pk=nurture_id)[0]
				get_data = NurtureSerializer(nurture_data)
			else:
				nurture_data = Nurture.objects.filter(is_deleted=True)
				get_data = NurtureSerializer(nurture_data,many=True)
			return ApiResponse().success(get_data.data,200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting the company details",500)

	def put(self,request,nurture_id):
		try:
			get_data = Nurture.objects.get(pk=nurture_id)
			update_data = NurtureSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Nurture details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.errors,400)	
		except:
			return ApiResponse().error("Error while updating the company details",500)

	def delete(self,request,nurture_id):
		try:
			Nurture.objects.filter(pk=nurture_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 400)


class NurtureUrlApi(APIView):
	def post(self,request):
		try:
			nurture_data = NurtureUrlSerializer(data=request.data)
			if not(nurture_data.is_valid()):
				return ApiResponse().error(nurture_data.errors,400)
			nurture_data.save()
			return ApiResponse().success("Nurtureurl added successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding Nurtureurl",400)

	def get(self,request,nurtureurl_id=None):
		try:
			if(nurtureurl_id):
				nurture_data = NurtureUrl.objects.filter(is_deleted=False,pk=nurtureurl_id)[0]
				get_data = NurtureUrlSerializer(nurture_data)
			else:
				nurture_data = NurtureUrl.objects.filter(is_deleted=False)
				get_data = NurtureUrlSerializer(nurture_data,many=True)
			return ApiResponse().success(get_data.data,200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting the Nurtureurl details",500)

	def put(self,request,nurtureurl_id):
		try:
			get_data = NurtureUrl.objects.get(pk=nurtureurl_id)
			update_data = NurtureUrlSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Nurtureurl details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.errors,400)	
		except:
			return ApiResponse().error("Error while updating the Nurtureurl details",500)

	def delete(self,request,nurtureurl_id):
		try:
			NurtureUrl.objects.filter(pk=nurtureurl_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 400)








