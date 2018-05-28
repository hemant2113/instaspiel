from django.core.management.base import BaseCommand
from app.roles.models import Role
from app.users.models import UserProfile
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
		roles.append(Role(name="Superadmin"))
		roles.append(Role(name="Subadmin"))
		roles.append(Role(name="Company admin"))
		roles.append(Role(name="Company subadmin"))
		roles.append(Role(name="Visitor"))
		Role.objects.bulk_create(roles)


	def insertDataMasterUser(self):
		try:
			if(UserProfile.objects.all().count() > 0):
				return "Data has already exists in db"
		except:
			pass		
		email = "admin6@gmail.com"
		user = User.objects.create_user(username=email,email=email,password=12345)
		userProfile = UserProfile(first_name="admin",role=Role.objects.get(id=1),last_name="admin",status=True,user = user)
		userProfile.save()


	def handle(self,*args,**options):
		self.insertData()
		self.insertDataMasterUser()	
		print ('data inserted')
