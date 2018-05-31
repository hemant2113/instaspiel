from rest_framework import serializers
from app.company.models import Company
from app.company.models import AssignCompanies
from app.nurture.models import Nurture
from app.nurture.serializers import NurtureSerializer,NurtureDataSerializer

class CompanySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Company
		fields = ('id','name','logo','favicon','url','header_script','body_script','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			'url': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
		# 	'logo': {
		# 		'required':True,
		# 		'error_messages':{
		# 		'required':"Please fill this field",
		# 		}
		# 	},
		}		

class CompanyDetailSerializer(serializers.ModelSerializer):
	nurture_data = serializers.SerializerMethodField("getNurtureData")
	def getNurtureData(self, obj):
		try:
			return NurtureSerializer(Nurture.objects.filter(is_deleted=False,company=obj.id)[0]).data
		except Exception as err :
			print(err)
			return None	

	class Meta:
		model = Company
		fields = ('id','name','nurture_data','logo','favicon','url','header_script','body_script','is_deleted','created_at','updated_at')


class AssignCompanySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = AssignCompanies
		fields = ('id','user','company','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'user': {
				'required':True,
				'error_messages':{
				'required':"Please fill user_id field",
				}
			},
			'company': {
				'required':True,
				'error_messages':{
				'required':"Please put fill company_id field",
				}
			},
			
		}			