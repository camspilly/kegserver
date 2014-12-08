from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
  url(r'^register/', views.register, name='register'),
  url(r'^resetpin/', views.resetpin, name='resetpin'),
  url(r'^login/', views.login, name='login'),
  url(r'^pin/', views.pinToUser, name='pinToUser'),
  url(r'^purchase/', views.purchase, name='purchase'),
  url(r'^$', views.index, name='index')
)

