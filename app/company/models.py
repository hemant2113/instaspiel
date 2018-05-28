from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Company(models.Model):
	name = models.CharField(max_length=100,default='')
	logo = models.ImageField(upload_to = 'pic_folder/', default ='pic_folder/no-img.jpg')
	favicon = models.ImageField(upload_to = 'pic_folder/', default ='pic_folder/no-img.jpg')
	url = models.TextField(null=True,blank=True)
	header_script = models.TextField(null=True,blank=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)


class AssignCompanies(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company,blank=True,null=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		managed = True
		db_table = 'assign_companies'
