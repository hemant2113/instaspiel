from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.nurture.serializers import NurtureSerializer,NurtureUrlSerializer,NurtureDetailSerializer
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from app.nurture.models import Nurture,NurtureUrl
from app.lib.response import ApiResponse
from app.lib.common import AccessUserObj, RequestOverwrite
from app.users.models import UserProfile
import re
from rest_framework.decorators import authentication_classes, permission_classes
from app.users.permissions import IsAuthenticatedOrCreate


class NurtureApi(APIView):
	def split_special_character(self, value):
		if value:
			result = re.sub(r'\W+', '-', value.strip())
			return result.strip('-')
		return None	
	# permission_classes = (IsAuthenticatedOrCreate, )
	def post(self,request):
		try:
			# user = AccessUserObj().fromToken(request).user
			# user_id = UserProfile.objects.get(user_id = user.id)
			# print(user.id)
			# if (user_id.role.id == 3) or (user_id.role.id == 1):

			if request.data.get('name'):
				nurture_name = self.split_special_character(request.data.get('name'))
				RequestOverwrite().overWrite(request, {'nurture_name_show':nurture_name})
			nurture_data = NurtureDetailSerializer(data = request.data)
			if not(nurture_data.is_valid()):
				return ApiResponse().error(nurture_data.errors,400)
			nurture_data.save()
			if(request.data.get('nurture_url')):
				urlData = []
				nurture = Nurture.objects.get(id = nurture_data.data.get('id'))
				print(nurture)
				for nurl in request.data.get('nurture_url'):		
					nurture_url = NurtureUrl()
					nurture_url.hubspot_check_form = nurl['hubspot_check_form']
					nurture_url.name = nurl['name'].strip()
					nurture_url.url_name_show = self.split_special_character(nurl['name'])
					doc_script = None
					try:
						doc_script = nurl['doc_script'].strip()
					except Exception as err:
						print(err)	
					# if nurl['url'] and ".pdf" in nurl['url']:
					# 	nurture_url.url = "https://docs.google.com/viewer?url="+nurl['url']+"&embedded=true"		
					# else:
					# 	nurture_url.url = nurl['url'].strip()
					nurture_url.url = nurl['url'].strip()
					nurture_url.doc_script = doc_script
					nurture_url.nurture = nurture
					urlData.append(nurture_url) 
				NurtureUrl.objects.bulk_create(urlData)
			return ApiResponse().success(nurture_data.data, 200)
			# return ApiResponse().error("You are not authorised to create nurture", 400)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding nurture", 500)

	def get(self,request,nurture_id=None):
		try:
			if(nurture_id):
				try:
					get_data = NurtureDetailSerializer(Nurture.objects.get(is_deleted=False,id=nurture_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid nurture id", 400)
			else:
				nurture_data = Nurture.objects.filter(is_deleted=False)
				get_data = NurtureDetailSerializer(nurture_data, many=True)
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Nurture does not exists", 500)

	permission_classes = (IsAuthenticatedOrCreate, )		
	def put(self,request,nurture_id):
		try:
			get_data = Nurture.objects.get(pk=nurture_id)
			if request.data.get('name'):
				nurture_name = self.split_special_character(request.data.get('name'))
				RequestOverwrite().overWrite(request, {'nurture_name_show':nurture_name})
			update_data = NurtureDetailSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				if(request.data.get('nurture_url_1')):
					for nurl in request.data.get('nurture_url_1'):
						url_name_show = self.split_special_character(nurl['name'])
						doc_script = None
						try:
							doc_script = nurl['doc_script'].strip()
						except Exception as err:
							print(err)

						try:
							NurtureUrl.objects.filter(id = nurl['id']).update(name = nurl['name'].strip(),url_name_show = url_name_show, url = nurl['url'].strip(),doc_script=doc_script,hubspot_check_form=nurl['hubspot_check_form'])
							# NurtureUrl.objects.filter(id = nurl['id']).update(name = nurl['name'], url = nurl['url'])
							continue
						except Exception as err:
							print(err)	
						
				if(request.data.get('nurture_url_2')):
					urlData = []
					nurture = Nurture.objects.get(id = nurture_id)
					for nurl in request.data.get('nurture_url_2'):
						# print(nurl)
						nurture_url = NurtureUrl()
						if not nurl['name'] and not nurl['url']:
							continue
						# if nurl['name']:
						# 	url_name = re.sub(r'\W+', '-', nurl['name'].strip())
						# 	nurture_url.split_special_character = url_name
						nurture_url.url_name_show = self.split_special_character(nurl['name'])
						# if nurl['url'] and ".pdf" in nurl['url']:
						# 	nurture_url.url ="https://docs.google.com/viewer?url="+nurl['url']+"&embedded=true"		
						# else:
						# 	nurture_url.url = nurl['url']
						# nurture_url.url_name_show=nurl['url_name_show']
						doc_script = None
						try:
							doc_script = nurl['doc_script'].strip()
						except Exception as err:
							print(err)
						nurture_url.hubspot_check_form = nurl['hubspot_check_form']	
						nurture_url.name = nurl['name'].strip() 
						nurture_url.url = nurl['url'].strip()
						nurture_url.doc_script = doc_script
						nurture_url.nurture = nurture
						urlData.append(nurture_url) 
					NurtureUrl.objects.bulk_create(urlData)

				return ApiResponse().success("Nurture details updated Successfully", 200)
			else:
				return ApiResponse().error(update_data.errors, 400)	
		except Exception as err:
			print(err)
			return ApiResponse().error("Error", 500)

	permission_classes = (IsAuthenticatedOrCreate, )		
	def delete(self,request,nurture_id):
		try:
			Nurture.objects.filter(pk=nurture_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)

class NurtureDataByCompanyId(APIView):
	# permission_classes = (IsAuthenticatedOrCreate, )
	def get(self,request,company_id=None):
		try:
			if(company_id):
				try:
					nurture_data = Nurture.objects.filter(is_deleted=False, company_id=company_id)
					get_data = NurtureSerializer(nurture_data, many=True)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide company id", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Nurture matching query does not exist", 500)

class NurtureByCompanyName(APIView):
	def get(self,request,company_name=None):
		try:
			if(company_name):
				try:
					nurture_data = Nurture.objects.filter(is_deleted=False, company__name=company_name)
					get_data = NurtureSerializer(nurture_data, many=True)
					print(get_data.data)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide company Name", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Nurture matching query does not exist", 500)


class NurtureUrlApi(APIView):
	# permission_classes = (IsAuthenticatedOrCreate, )
	def post(self,request):
		try:
			# if ".pdf" in request.data.get('url'):
			# 	nurture_url = "https://docs.google.com/viewer?url="+request.data.get('url')+"&embedded=true"
			# 	RequestOverwrite().overWrite(request, {'url':nurture_url})
		
			nurture_data = NurtureUrlSerializer(data=request.data)
			if not(nurture_data.is_valid()):
				return ApiResponse().error(nurture_data.errors, 400)
			nurture_data.save()
			return ApiResponse().success(nurture_data.data, 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while adding Nurtureurl", 500)

	def get(self,request,nurtureurl_id=None):
		try:
			if(nurtureurl_id):
				try:
					get_data = NurtureUrlSerializer(NurtureUrl.objects.get(is_deleted=False,pk=nurtureurl_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid nurture url id", 400)
			else:
				nurture_data = NurtureUrl.objects.filter(is_deleted=False)
				get_data = NurtureUrlSerializer(nurture_data,many=True)
			
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Error while getting nurture url", 500)

	def put(self,request,nurtureurl_id):
		try:
			get_data = NurtureUrl.objects.get(pk=nurtureurl_id)
			update_data = NurtureUrlSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Nurtureurl details updated Successfully",200)
			else:
				return ApiResponse().error(update_data.data, 400)	
		except:
			return ApiResponse().error("Error", 500)

	permission_classes = (IsAuthenticatedOrCreate, )		
	def delete(self,request,nurtureurl_id):
		try:
			NurtureUrl.objects.filter(pk=nurtureurl_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)


class UrlByNurture(APIView):
	# permission_classes = (IsAuthenticatedOrCreate, )
	def get(self,request,nurture_id=None):
		try:
			if(nurture_id):
				try:
					nurtureurl_data = NurtureUrl.objects.filter(is_deleted=False, nurture_id=nurture_id)
					get_data = NurtureUrlSerializer(nurtureurl_data, many=True)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide nurture id", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("NurtureUrl matching query does not exist", 500)


class UrlByNurtureShow(APIView):
	def get(self,request,nurture_name_show=None):
		try:
			if(nurture_name_show):
				try:
					nurtureurl_data = NurtureUrl.objects.filter(is_deleted=False, nurture__nurture_name_show=nurture_name_show)
					get_data = NurtureUrlSerializer(nurtureurl_data, many=True)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide nurture name", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("NurtureUrl matching query does not exist", 500)
