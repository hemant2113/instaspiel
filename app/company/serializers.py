from rest_framework import serializers
from app.company.models import Company,AssignCompanies
from app.nurture.models import Nurture
from app.nurture.serializers import NurtureSerializer,NurtureUrlSerializer
from django.core.exceptions import ValidationError


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

	def validate_url(self,url):
		url = url.strip()
		company = Company.objects.filter(url__iexact = url.lower(), is_deleted = False)
		if (self.context) and (self.context['company_id'])  is not None:
			company = company.exclude(id = self.context['company_id'])
		company.exists()
		if company is True or len(company)>0:
			raise  ValidationError('This url already exists.', code='invalid')
		return url	

	def validate_name(self, name):
		name = name.strip()
		company = Company.objects.filter(name__iexact = name.lower(), is_deleted = False)
		if (self.context) and (self.context['company_id'])  is not None:
			company = company.exclude(id = self.context['company_id'])
		company.exists()
		if company is True or len(company)>0:
			raise  ValidationError('This company name already exists.', code='invalid')
		return name		

class CompanyDetailSerializer(serializers.ModelSerializer):
	nurture_data = serializers.SerializerMethodField("getNurtureData")
	def getNurtureData(self, obj):
		try:
			return NurtureSerializer(Nurture.objects.filter(is_deleted=False,company=obj.id),many=True).data
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