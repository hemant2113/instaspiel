from rest_framework import serializers
from app.nurture.models import Nurture,NurtureUrl


class NurtureSerializer(serializers.ModelSerializer):
	nurture_url = serializers.SerializerMethodField("getNurtureUrl")
	def getNurtureUrl(self, obj):
		try:
			return NurtureUrlSerializer(NurtureUrl.objects.filter(is_deleted= False,nurture=obj.id)[:5], many=True).data
		except Exception as err :
			print(err)
			return None	
	
	class Meta:
		model = Nurture
		fields = ('id','name','company','nurture_url','description','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			'description': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			'company': {
				'required':True,
				'error_messages':{
				'required':"Please provide company id",
				}
			},
		}		

class NurtureDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Nurture
		fields = ('id','name','description','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			'description': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			'company': {
				'required':True,
				'error_messages':{
				'required':"Please provide company id",
				}
			},
		}		

class NurtureUrlSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = NurtureUrl
		fields = ('id','name','url','nurture','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'url': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			},
			
		}		

