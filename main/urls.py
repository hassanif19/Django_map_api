from django.urls import path 
from . import views

 
app_name = "main"

urlpatterns = [
	
	path('', views.route, name="route"),
	path('map', views.map, name="map"),
	# path('mail', views.Index.as_view(), name='index'),
	path('contact', views.contact_view.as_view(), name="contact"),
	# path('station', views.adresses, name="station"),
    path('station', views.AdresseAPIView.as_view(), name="station"),
	 
	path('station/<str:id>/', views.AdresseDetails.as_view(), name="station"),
     
	]