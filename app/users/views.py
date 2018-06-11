from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from app.users.serializers import ProfileSerializer,UserSerializer
from app.users.models import UserProfile
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from app.lib.response import ApiResponse
from app.lib.common import AccessUserObj,RequestOverwrite
from app.lib.email import Email
from functools import wraps
from rest_framework.decorators import authentication_classes, permission_classes
from app.lib.permissions import IsAuthenticatedOrCreate

class UserApi(APIView):
	
	def post(self,request):
		try:
			# user_token = AccessUserObj().fromToken(request).user
			# user_id = UserProfile.objects.get(user_id = user_token.id)
			# print(user_token.id)
			# if (user_id.role.id == 3) or (user_id.role.id == 1):
			# email = request.data.get('email')
			# password = request.data.get('password')
			# print(email,password)
			# if (email.is_valid()) and (password.is_valid()):
			# 	if not len(request.data.get('password'))>=6:
			# 		return ApiResponse().error("Please fill minimum password lenght six", 400)
			# print(type(request.data.get('role')))
			# print(request.data.get('company'))
			# print("==========")
			# import pdb;pdb.set_trace();
			# if int(request.data.get('role'))==3 or int(request.data.get('role'))==4 and request.data.get('company'): 
			user_info = UserSerializer(data = request.data)
			if not user_info.is_valid():
				return ApiResponse().error(user_info.errors,400)
			user = self.create_user(request)
			if not(user):
				return ApiResponse().error("This email is already exists", 400)
			RequestOverwrite().overWrite(request, {'user':user.id})
			user_data = ProfileSerializer(data=request.data)
			if not(user_data.is_valid()):
				return ApiResponse().error(user_data.errors, 400)
			user_data.save()
			email = request.data.get('email')
			password = request.data.get('password')
			frm = 'instaspiel@gmail.com'
			try:
				body = "Hello"+" "+request.data.get('first_name')+" "+request.data.get('last_name')+"\n We would like to welcome you as a new member of "+user_data['company_name'].value+"\n Username:- "+email+"\n Password:- "+password+""

				if Email.sendMail("Account created successfully",body,frm,email) is True:
					return ApiResponse().success(user_data.data, 200)
				return ApiResponse().error("Error while sending the email", 400)
			except Exception as err:
				print(err)
				return ApiResponse().error("Please send valid company id",400)
			# elif int(request.data.get('role'))==1 or int(request.data.get('role'))==5 or int(request.data.get('role'))==2 and not (request.data.get('company')): 
			# 	user_info = UserSerializer(data = request.data)
			# 	if not user_info.is_valid():
			# 		return ApiResponse().error(user_info.errors,400)
			# 	user = self.create_user(request)
			# 	if not(user):
			# 		return ApiResponse().error("This email is already exists", 400)
			# 	RequestOverwrite().overWrite(request, {'user':user.id})
			# 	user_data = ProfileSerializer(data=request.data)
			# 	# print(user_data)
			# 	if not(user_data.is_valid()):
			# 		return ApiResponse().error(user_data.errors, 400)
			# 	user_data.save()	
			# 	email = request.data.get('email')
			# 	password = request.data.get('password')
			# 	frm = 'instaspiel@gmail.com'
			# 	body = "Hello"+" "+request.data.get('first_name')+" "+request.data.get('last_name')+"\n We would like to welcome you as a new member"+""+"\n Username:- "+email+"\n Password:- "+password+""
			# 	if Email.sendMail("Account created successfully",body,frm,email) is True:
			# 		return ApiResponse().success(user_data.data, 200)
			# 	return ApiResponse().error("Error while sending the email", 400) 
			# return ApiResponse().error("Please send valid role id",400)
			# return ApiResponse().success(user_data.data, 200)
			# except Exception as err:
			# 	print(err)
			# return ApiResponse().error("Please send valid company id",400)  
		# return ApiResponse().error("you are not company admin", 400)
		except Exception as err:
			print(err)
			return ApiResponse().error("There is a problem while creating user", 500)


	def create_user(self,request):
		try:
			user = User.objects.create_user(username=request.data.get('email'),
			email=request.data.get('email'),password=request.data.get('password'),is_staff=True)
			return user
		except Exception as err:
			print(err)
			return None

	def get(self,request,user_id=None):
		permission_classes = (IsAuthenticatedOrCreate, )
		try:
			if(user_id):
				try:
					user_data = ProfileSerializer(UserProfile.objects.get(is_deleted=False, user=user_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid user id", 400)
			else:
				userData = UserProfile.objects.filter(is_deleted=False)
				user_data = ProfileSerializer(userData, many=True)
			return ApiResponse().success(user_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error", 500)

	def put(self,request,user_id):
		permission_classes = (IsAuthenticatedOrCreate, )
		try:
			if(request.data.get('email')):
				try:
					user = User.objects.get(email=request.data.get('email'))
					if int(user_id) != int(user.id):
						return ApiResponse().error("This email is already exists", 400)
				except Exception as err:
					print(err)
				get_data = UserProfile.objects.get(user=user_id)
				RequestOverwrite().overWrite(request, {'user':user_id})
				print(request.data)
				User.objects.filter(id = user_id).update(email = request.data.get('email'), username = request.data.get('email')) 
				update_data = ProfileSerializer(get_data,data=request.data)
				if update_data.is_valid():
					update_data.save()
					return ApiResponse().success(update_data.data, 200)
				else:
					return ApiResponse().error(update_data.errors, 400)	
		except Exception as err:
			print(err)
			return ApiResponse().error("Error", 500)

	def delete(self,request,user_id):
		try:
			UserProfile.objects.filter(user=user_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)

class UserCompanyApi(APIView):

	def get(self,request,company_id=None):
		try:
			if(company_id):
				userprofile = UserProfile.objects.filter(is_deleted=False, company=company_id)
				user_data = ProfileSerializer(userprofile, many=True)
			else:
				return ApiResponse().error("please send company id", 400)
			return ApiResponse().success(user_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error",500)


class LoginApi(APIView):
	permission_classes = (IsAuthenticatedOrCreate, )
	def post(self,request):
		try:
			# if not len(request.data.get('password'))>=6:
			# 	return ApiResponse().error("Required maximum password lenght is six", 400)
			if request.data.get('email') and request.data.get('password'):
				user = UserSerializer(data = request.data)
				if not user.is_valid():
					return ApiResponse().error(user.errors,400)
				try:
					auth_user = authenticate(username=request.data.get('email'), password=request.data.get('password'))
				except Exception as err:
					print(err)
					return ApiResponse().error("Invalid username or password",400)			
				if not auth_user:
					return ApiResponse().error("invalid username or password", 400)	
	
				token,create = Token.objects.get_or_create(user_id=auth_user.id)	
				if(auth_user):
					try:
						userprofile = UserProfile.objects.get(user_id=auth_user.id, is_deleted=False)
						user_data = ProfileSerializer(userprofile)
					except Exception as err:
						print(err)	
						return ApiResponse().error("invalid email or password", 400)

				token_value = {
					'token':token.key,
					}
				user_response = user_data.data
				user_response.update(token_value)
				return ApiResponse().success(user_response, 200)
			return ApiResponse().error("Please send correct email and password", 400)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while login", 500)

class LogOut(APIView): 
	
	def post(self,request):
		try:
			user = AccessUserObj().fromToken(request).user.id
			if not user:
				return ApiResponse().error('Token matching query does not exist', 400)
			Token.objects.filter(user = user).delete()
			return ApiResponse().success("Logout Successfully", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error', 500)

class CheckEmail(APIView):
	
	def post(self,request):
		try:
			user = User.objects.get(username=request.data.get('email'))
			UserProfile.objects.filter(user=user.id, is_deleted=False)
			return ApiResponse().success(True, 200)
		except Exception as err:
			print(err)
			return ApiResponse().success(False, 200)

class ChangePassword(APIView):

	def post(self,request):
		try:
			user = AccessUserObj().fromToken(request).user
			if not request.data.get("old_password"):
				return ApiResponse().error("Please enter current password.",400)
			if UserProfile.objects.filter(is_deleted=True, user=user):
				return ApiResponse().success("User does not exist",400) 
			if request.data.get("old_password") is not None:
				if authenticate(username = user, password = request.data.get("old_password")) is None:
					return ApiResponse().error("Invalid current password entered.",400)
			password = request.data.get("new_password")
			confirm_new_password = request.data.get("confirm_new_password")
			if password != '' and confirm_new_password !='':
				if len(password)>=6 and len(confirm_new_password)>=6:
					if password != confirm_new_password:
						return ApiResponse().success("New Password and Confirm Password does not match",400)
					user.set_password(request.data.get("new_password"))
					user.save()
					return ApiResponse().success("password changed successfully", 200)
				return ApiResponse().error("Please Fill Minimum Password length Six", 400)
			return ApiResponse().error("Password empty", 400)   
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while change password", 500)


class ForGotPassword(APIView):
	def post(self,request):
		try:
			user = User.objects.get(email = request.data.get("email"))
		except Exception as err:
			return ApiResponse().error("This email is not registered", 400)
		password = User.objects.make_random_password()
		print(password)
		user.set_password(password)
		user.save()
		frm = 'instaspiel@gmail.com'
		body = "Hi there. \n You have requested a new password for your account on Instaspiel.\nYour temporary password is "+password+""
		if Email.sendMail("Forgot password",body,frm,user.email) is True:
		    return ApiResponse().success("New password was sent to your email",200)    
		return ApiResponse().error("Error while sending the email",500) 
		

class UserRole(APIView):
	def post(self,request):
		try:
			user = AccessUserObj().fromToken(request).user
			user_id = UserProfile.objects.get(user_id = user.id)
			if (user_id.role.id == 3):
				return ApiResponse().success("you can create user and nurture", 200)
			return ApiResponse().error("You are not authorised to create user and nurture", 400)
		except Exception as err:
			return ApiResponse().error("Error", 500) 

class CurrentPassword(APIView):
	def post(self,request):
		try:
			user = AccessUserObj().fromToken(request).user
			if not request.data.get("password"):
				return ApiResponse().error("Please enter valid current password.",400)
			if UserProfile.objects.filter(is_deleted=True, user=user):
				return ApiResponse().success("User does not exist",400) 
			if request.data.get("password") is not None:
				if authenticate(username = user, password = request.data.get("password")) is None:
					return ApiResponse().error("Invalid current password entered.",400)
			return ApiResponse().success(True, 200)
		except Exception as err:
			print(err)
			return ApiResponse().success(False, 200)