from django.core.management.base import BaseCommand
from apps.roles.models import Role
from apps.users.models import UserProfile
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.contrib.auth.models import User


class Command(BaseCommand):
	args ='';
	help='For insert data in role model'


	def insertData(self):
		try:
			if(Role.objects.all().count() > 0):
				return "Data has already exists in db"
		except:
			pass		

		roles = [];
		roles.append(Role(name="admin"))
		roles.append(Role(name="user"))
		roles.append(Role(name="visitor"))
		Role.objects.bulk_create(roles)


	def insertDataMasterUser(self):
		try:
			if(UserProfile.objects.all().count() > 0):
				return "Data has already exists in db"
		except:
			pass		
		email = "admin@gmail.com"
		user = User.objects.create_user(username=email,email=email,password=12345,is_staff=True)
		userProfile = UserProfile(first_name="admin",role=Role.objects.get(id=1),last_name="admin",status=True,user = user)
		userProfile.save()


	def handle(self,*args,**options):
		self.insertData()
		self.insertDataMasterUser()	
		print ('data inserted')
