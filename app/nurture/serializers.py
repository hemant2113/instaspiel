from rest_framework import serializers
from app.nurture.models import Nurture,NurtureUrl


class NurtureSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Nurture
		fields = ('id','name','company','description','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			
		}		


class NurtureUrlSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = NurtureUrl
		fields = ('id','name','url','nurture','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			
		}		

