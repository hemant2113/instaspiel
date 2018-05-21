from rest_framework import serializers
from app.roles.models import Role

class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Role
		fields = ('id','name','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please insert your role",
				}
			}
		}