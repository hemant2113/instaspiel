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

	user_data = serializers.SerializerMethodField("getUserData")
	def getUserData(self,obj):
		try:
			return User.objects.get(id=obj.user.id).email
		except Exception as e:
			print(e)
	
	class Meta:
		model = UserProfile
		fields = ('id','user','role','company','user_data','role_name','first_name','last_name','is_deleted','created_at','updated_at','status')
		extra_kwargs = {
			'role': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			
			'user_data': {
				'required':True,
				'error_messages':{
				'required':"This field is required"
				}
			},
			
		}

