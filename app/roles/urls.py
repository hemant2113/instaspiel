from django.conf.urls import url
from app.roles import views
app_name='roles'

urlpatterns = [
	url(r'',views.RoleView.as_view()),
	
]
