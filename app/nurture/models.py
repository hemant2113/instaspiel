from django.db import models
from datetime import datetime
from app.company.models import Company

class Nurture(models.Model):

	company = models.ForeignKey(Company)
	name = models.CharField(max_length=500)
	nurture_name_show = models.CharField(max_length=500,null=True,blank=True)
	description = models.TextField(null=True,blank=True)
	hubspot_form = models.TextField(null=True,blank=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		managed = True
		db_table = 'nurture'
		ordering = ['id']

class NurtureUrl(models.Model):

	nurture = models.ForeignKey(Nurture)
	name = models.CharField(max_length=500,null=True,blank=True)
	url_name_show = models.CharField(max_length=500,null=True,blank=True)
	url = models.TextField(null=True,blank=True)
	doc_script = models.TextField(null=True,blank=True)
	hubspot_check_form = models.NullBooleanField(blank=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(default=datetime.now)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		managed = True
		db_table = 'nurture_url'
		ordering = ['id']
