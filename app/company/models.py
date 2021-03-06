from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

class Company(models.Model):
	name = models.CharField(db_index=True, max_length=255)
	logo = models.TextField(null=True,blank=True)
	favicon = models.TextField(null=True,blank=True)
	url = models.TextField(db_index=True,blank=True)
	header_script = models.TextField(null=True,blank=True)
	body_script = models.TextField(null=True,blank=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class AssignCompanies(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company,blank=True,null=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		managed = True
		db_table = 'assign_companies'
