from rest_framework import serializers
from app.users.models import UserProfile
from app.roles.models import Role
from django.contrib.auth.models import User
from app.company.serializers import CompanySerializer
from app.company.models import Company

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('email','id','password')
		extra_kwargs = {
			
			'email': {
				'required':True,
				'error_messages':{
				'required':"Email field is required"
				}
			},
			
		}


class ProfileSerializer(serializers.ModelSerializer):
	role_name = serializers.SerializerMethodField("getRoleName")
	def getRoleName(self,obj):
		try:
			return Role.objects.get(id=obj.role.id).name
		except Exception as e:
			print(e)

	email = serializers.SerializerMethodField("getEmail")
	def getEmail(self,obj):
		try:
			return User.objects.get(id=obj.user.id).email
		except Exception as e:
			print(e)

	company_name = serializers.SerializerMethodField("getCompanyName")
	def getCompanyName(self,obj):
		try:
			return Company.objects.get(id = obj.company.id).name
		except Exception as e:
			print(e)

	class Meta:
		model = UserProfile
		fields = ('id','user','role','company','company_name','email','role_name','first_name','last_name','is_deleted','created_at','updated_at','status')
		extra_kwargs = {
			# 'role': {
			# 	'required':True,
			# 	'error_messages':{
			# 	'required':"Please fill this field",
			# 	}
			# },
			
			'email': {
				'required':True,
				'error_messages':{
				'required':"This field is required"
				}
			},
			
		}

