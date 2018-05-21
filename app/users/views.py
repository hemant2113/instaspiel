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

class UserApi(APIView):

	def post(self,request):
		try:
			user = self.create_user(request)
			if not(user):
				return ApiResponse().error("Error while create user",500)
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
	def post(self,request,*args, **kwargs):
		try:
			email = request.data.get('email')
			password = request.data.get('password')
			if email:
				user = User.objects.get(username=email)
				try:
					auth_user = authenticate(username=email, password=password)
				except Exception as err:
					print(err)
					return ApiResponse().error('username or password incorrect')
				if not(auth_user):
					return ApiResponse().error('username or password incorrect')
				token,created = Token.objects.get_or_create(user_id=user.id)
				print(token)
				if(user):
					userprofile = UserProfile.objects.get(user_id=user.id)
					user_data = UserSerializer(userprofile)
				else:
					userData = UserProfile.objects.all()
					user_data = UserSerializer(userData,many=True)
				token_value = {
					'token':token.key,
					}
				user_response = user_data.data
				user_response.update(token_value)
				return ApiResponse().success(user_response,200)
			return ApiResponse().error("Error", 400)	
		except Exception as e:
			print(e)
			return ApiResponse().error("Error", 500)
					
