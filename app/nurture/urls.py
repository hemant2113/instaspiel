from django.conf.urls import url
from . import views

app_name='company'

urlpatterns = [
	url(r'^url/show/(?P<nurture_name_show>[a-zA-Z\s\w\-]+)$',views.UrlByNurtureShow.as_view()),
	url(r'^nurture/lists/(?P<company_name>[a-zA-Z\s\w\-]+)$',views.NurtureByCompanyName.as_view()),
	url(r'^nurture$',views.NurtureApi.as_view()),
	url(r'^nurtureurl/list/(?P<nurture_id>[0-9]+)$',views.UrlByNurture.as_view()),
	url(r'^nurture/list/(?P<company_id>[0-9]+)$',views.NurtureDataByCompanyId.as_view()),
	url(r'^nurture/(?P<nurture_id>[0-9]+)$',views.NurtureApi.as_view()),
	url(r'^nurture/url/(?P<nurtureurl_id>[0-9]+)$',views.NurtureUrlApi.as_view()),
	url(r'^nurture/url$',views.NurtureUrlApi.as_view()),
]











