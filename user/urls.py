from django.conf.urls import url
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.user_page, name="user_page"),
    url(r'^api/sign_in$', views.sign_in, name="sign_in"),
    url(r'^api/sign_up$', views.sign_up, name="sign_up"),
    url(r'^api/sign_out$', views.sign_out, name="sign_out"),
    url(r'^setting$', views.setting_page, name="setting_page"),
]
