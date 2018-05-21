from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from app.roles.models import Role
from app.company.models import Company

class UserProfile(models.Model):

	user = models.ForeignKey(User)
	role = models.ForeignKey(Role,default='')
	company = models.ForeignKey(Company)
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	status = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		managed = True
		db_table = 'user_profile'

