from django.db import models
from datetime import datetime


class Role(models.Model):
	name = models.CharField(max_length=45)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)

