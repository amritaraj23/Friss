from django.conf.urls import url
from basicapp import views

#TEMPLATE_URLS!
app_name = 'basicapp'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^formpage/',views.form_name_view,name='form_name')
]