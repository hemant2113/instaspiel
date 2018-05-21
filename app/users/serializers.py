from rest_framework import serializers
from app.users.models import UserProfile
from app.roles.models import Role
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	role_name = serializers.SerializerMethodField("getRoleName")
	def getRoleName(self,obj):
		try:
			return Role.objects.get(id=obj.role.id).name
		except Exception as e:
			print(e)

	user_name = serializers.SerializerMethodField("getUserName")
	def getUserName(self,obj):
		try:
			
			return User.objects.get(id=obj.user.id).username
		except Exception as e:
			print(e)
	
	class Meta:
		model = UserProfile
		fields = ('id','user','role','company','user_name','role_name','first_name','last_name','is_deleted','created_at','updated_at','status')
		extra_kwargs = {
			'role': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			'first_name': {
				'required':True,
				'error_messages':{
				'required':"first name is required",
				}
			},
			'last_name': {
				'required':True,
				'error_messages':{
				'required':"last name is required"
				}
			},
		}	