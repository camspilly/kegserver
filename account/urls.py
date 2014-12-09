from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
  url(r'^register/', views.register, name='register'),
  url(r'^resetpin/', views.resetpin, name='resetpin'),
  url(r'^login/', views.login, name='login'),
  url(r'^pin/', views.pinToUser, name='pinToUser'),
  url(r'^purchase/', views.purchase, name='purchase'),
  url(r'^add_payment', views.add_payment, name='add_payment'),
  url(r'^remove_payment', views.remove_payment, name='remove_payment'),
  url(r'^$', views.index, name='index')
  

)

