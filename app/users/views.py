from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from app.users.serializers import UserSerializer
from app.users.models import UserProfile
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from app.lib.response import ApiResponse
from app.lib.common import AccessUserObj, RequestOverwrite




class UserApi(APIView):

	def post(self,request):
		try:
			user = self.create_user(request)
			if not(user):
				return ApiResponse().error("Error while create user",400)
			self.overWrite(request, {'user':user.id})
			user_data = UserSerializer(data=request.data)
			if not(user_data.is_valid()):
				return ApiResponse().error(user_data.errors,400)
			user_data.save()
			return ApiResponse().success(user_data.data,200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error",500)

	def overWrite(self, request, dic):
		try:
			try:
				if request.data._mutable is False:
					request.data._mutable = True
			except:
				pass
			for key,value in dic.items():
				request.data[key] = value
		except Exception as err:
			print(err)
			return False

	def create_user(self,request):
		try:
			return User.objects.create_user(username=request.data.get('email'),email=request.data.get('email'),password=request.data.get('password'))
		except Exception as err:
			print(err)
			return False

	def get(self,request,user_id=None):
		try:
			if(user_id):
				userprofile = UserProfile.objects.filter(is_deleted=False, pk=user_id)[0]
				user_data = UserSerializer(userprofile)
			else:
				userData = UserProfile.objects.filter(is_deleted=False)
				user_data = UserSerializer(userData, many=True)
			return ApiResponse().success(user_data.data,200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting the user details",500)

	def put(self,request,user_id):
		try:
			get_data = UserProfile.objects.get(pk=user_id)
			update_data = UserSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("User details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.errors,400)	
		except:
			return ApiResponse().error("Error while updating the user details",500)

	def delete(self,request,user_id):
		try:
			UserProfile.objects.filter(pk=user_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 400)

class LoginApi(APIView):
	# permission_classes = (IsAuthenticatedOrCreate, )
	def post(self,request):
		try:
			if request.data.get('email') and request.data.get('password'):
				try:
					auth_user = authenticate(username=request.data.get('email'), password=request.data.get('password'))
				except Exception as err:
					print(err)
					return ApiResponse().error("email or password invalid", 400)			
				token,create = Token.objects.get_or_create(user_id=auth_user.id)	
				print(token,create)
				if(auth_user):
					userprofile = UserProfile.objects.get(user_id=auth_user.id)
					user_data = UserSerializer(userprofile)
				else:
					userData = UserProfile.objects.all()
					user_data = UserSerializer(userData,many=True)
				token_value = {
					'token':token.key,
					}
				user_response = user_data.data
				user_response.update(token_value)
				print(user_response)
				return ApiResponse().success("success", 200)

			return ApiResponse().error("Please send email and password", 400)
		except Exception as err:
			print(err)
			return ApiResponse().error("user matching query does not exists", 500)

class LogOut(APIView):
	
	def post(self,request):
		try:
			user = AccessUserObj().fromToken(request).user.id
			res = Token.objects.filter(user = user).delete()
			return ApiResponse().success("Logout Successfully", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Token matching query does not exist', 500)

