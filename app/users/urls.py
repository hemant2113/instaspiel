from django.conf.urls import url
from . import views

app_name='users'

urlpatterns = [
	url(r'^userrole$',views.UserRole.as_view()),
	url(r'^checkemail$',views.CheckEmail.as_view()),
	url(r'^forgotpassword$',views.ForGotPassword.as_view()),
	url(r'^changepassword$',views.ChangePassword.as_view()),
	url(r'^logout$',views.LogOut.as_view()),
	url(r'^login$',views.LoginApi.as_view()),
	url(r'^user/(?P<user_id>[0-9]+)$',views.UserApi.as_view()),
	url(r'^user/company/(?P<company_id>[0-9]+)$',views.UserCompanyApi.as_view()),
	url(r'^user$',views.UserApi.as_view()),
]





