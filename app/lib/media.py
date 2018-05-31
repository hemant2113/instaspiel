from django.core.files.storage import default_storage
import boto
import boto.s3
import sys
from boto.s3.key import Key 
from django.conf import settings
from datetime import datetime
from app.lib.response import ApiResponse
from rest_framework.views import APIView
# from app.lib.permissions import SkipAuth
from rest_framework.decorators import authentication_classes, permission_classes
class MediaUpload(APIView):
	
	

	
	# permission_classes = (SkipAuth, )  	
	def post(self,request):
		try:
			print(request.FILES.getlist("files"))
			for i in request.FILES.getlist("files"):
				print(i)
			if request.data.get("destination") is None:
				return ApiResponse.error("Not getting any destination",400)
			destination = request.data.get("destination")
			if request.data.get("field") is None:
				return ApiResponse.error("Not getting any field",400)
			destination = request.data.get("destination")
			fieldname = request.data.get("field")

			AWS_ACCESS_KEY_ID = getattr(settings,"AWS_S3_ACCESS_KEY_ID")
			AWS_SECRET_ACCESS_KEY = getattr(settings,"AWS_S3_SECRET_ACCESS_KEY")
			AWS_S3_HOST = getattr(settings,"AWS_S3_HOST")
			bucket_name=getattr(settings,"AWS_STORAGE_BUCKET_NAME")
			
			filesList = request.FILES.getlist(fieldname)
			fileArray = []
			url = ''
			for files in filesList:
				conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
				AWS_SECRET_ACCESS_KEY , host=AWS_S3_HOST)
				bucket = conn.get_bucket(bucket_name)
				k = Key(bucket)
				fileName = str(int(datetime.today().timestamp())) + files.name 
				k.key = getattr(settings,"AWS_MAIN_DIR")+'/'+destination+'/'+fileName
				
				k.set_contents_from_file(files)
				url = 'https://'+getattr(settings,"AWS_BUCKET_URL")+'/'+k.key
				fileArray.append(url)
				conn.close()

			response = fileArray	
			if len(filesList) < 2:
				response = url


			return ApiResponse().success(response,200)
		except Exception as err:
			print(err)
			print("Error in mediaUpload class media method")
			return ApiResponse().error("Error while uploading media file",500)	


	def addTimeStamp(self,request,fieldname):
		try:
			files = request.FILES.get(fieldname)
			files.name = str(int(datetime.today().timestamp())) + files.name
			request.FILES[fieldname]  =  files 
			return request
		except Exception as err:
			print(err)
			print("Error in mediaUpload class and addTimeStamp method")	
			return request