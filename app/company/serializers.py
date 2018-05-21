from rest_framework import serializers
from app.company.models import Company


class CompanySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Company
		fields = ('id','name','logo','favicon','url','header_script','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			
		}		


		