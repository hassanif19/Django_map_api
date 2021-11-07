from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
import math
from .mixins import Directions
from django.core.mail import send_mail
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64
from matplotlib.ticker import LinearLocator
import numpy as np 
from main.serializers import AdresseSerializer
from main.models import Adresse 
import json
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from django.shortcuts import get_object_or_404
from .forms import ContactForm
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms

'''
Basic view for routing 
'''
def route(request):
      
  
	context = {"google_api_key": settings.GOOGLE_API_KEY, 
	           "serializer":adresses()}
	return render(request, 'main/route.html', context)


'''
Basic view for displaying a map 
'''
def map(request):

	lat_a = request.GET.get("lat_a")
	long_a = request.GET.get("long_a")
	lat_b = request.GET.get("lat_b")
	long_b = request.GET.get("long_b")
	vitesse = request.GET.get("vitesse")
	soc= request.GET.get("soc") 
	# station = Adresses.objects.all()
	# waypoints=request.GET.get("waypoints")
	puissance_vehicule=voiture(int(vitesse)) 
	autonomie_soc_initial =autonomie_soc_minimal(puissance_vehicule,int(soc))
  
    
	directions = Directions(
		lat_a= lat_a,
		long_a=long_a,
		lat_b = lat_b,
		long_b=long_b
		)
 
	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,
	"puissance_vehicule":puissance_vehicule, 
	"autonomie_soc_minimal":autonomie_soc_initial,
	"serializer":adresses()
	# "station":station
    # "waypoints":waypoints
	}
	return render(request, 'main/map.html', context)

def voiture(vitesse) :
	mass = 2000 #kgcd  
	mass_factor = 1.05
	acceleration = 0 # m^2 / s
	coeff_roll_R = 0.02  # coefficient of rolling resistance
	air_density = 1.225 # kg/m^3
	front_area = 2 # m^2
	aero_drag_coff = 0.5
	wind_speed = 0 # m/s
	road_angle = 0 # angle
	angle = 2       
	rad = math.radians(angle)
	p1 = (mass_factor * mass * acceleration) + (mass * 9.8 * coeff_roll_R * math.cos(rad))
	p2 = 0.5 * air_density * front_area * aero_drag_coff * ((vitesse -wind_speed)**2) # vitesse en m/S
	p3 = mass * 9.8 * math.sin(rad)
	puissance =round(((p1 + p2 + p3) * (vitesse/3.6) )/1000, 3) #kw
	return puissance

def batterie(puissance_vehicule, soc_initial, temps):
    
	capacite_totale =10 #KWH
	capacite_restante=(puissance_vehicule*temps)/3600  #KWH
	soc_batterie=soc_initial - (capacite_restante/capacite_totale )*100 # %
	return soc_batterie 

def autonomie_soc_minimal(puissance_vehicule, soc_initial):
	 
	capacite_totale =10 #KWH
	autonimie_soc_minimal=round(((36*capacite_totale*(soc_initial))/puissance_vehicule),2)
	return autonimie_soc_minimal

# def calcul(temps, soc_batterie):
	 
# 	fig, ax = plt.subplots(figsize=(10,4))
# 	ax.plot(temps,soc_batterie, '--bo')
# 	fig.autofmt_xdate()
# 	ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
# 	ax.set_title('Etat de décharge de la batterie')
# 	ax.set_ylabel("Soc (%)")
# 	ax.set_xlabel("Temps (min)")
# 	ax.set_ylim([0,110])
# 	ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
# 	ax.yaxis.set_minor_locator(LinearLocator(25))
# 	flike = io.BytesIO()
# 	fig.savefig(flike)
# 	b64 = base64.b64encode(flike.getvalue()).decode()
	 
# 	return b64

  
def adresses():


	qs1 = Adresse.objects.all()

	serializer = AdresseSerializer(qs1, many=True)
	
	pars = json.dumps(serializer.data,ensure_ascii=False)
	return pars
class ContactAPIView(APIView):

      def get(self, request):
          rq =Adresse.objects.all()
          serializer = AdresseSerializer(rq, many=True)
          return render(request, 'main/route.html', serializer.data)

      def post(self, request):
          serializer= AdresseSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
			  
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	

# 	return render(request,"main/index.html",{'serializer':pars})
 
    #  def post(self, request):
    #       serializer= AdresseSerializer(data=request.data)
    #       if serializer.is_valid():
        # serializer.save()
    #          return Response(serializer.data)
    #       return Response(serializer.errors) 
class AdresseAPIView(APIView):
    #   permission_classes = (IsAuthenticated, )
      def get(self, request):
          articles = Adresse.objects.all()
          serializer = AdresseSerializer(articles, many=True)
          return Response(serializer.data)

      def post(self, request):
          serializer= AdresseSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdresseDetails(APIView):
    
	def get_object(self, id):
		try:
		  return Adresse.objects.get(id=id)
		except Adresse.DoesNotExist:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	def get(self, request, id):
		station =self.get_object(id)
		serializer = AdresseSerializer(station)
		return Response(serializer.data)

	def put(self, request, id):
		station=self.get_object(id)
		serializer= AdresseSerializer(station, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	def delete(self,request, id):
          article =self.get_object(id)
          article.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)	

 
class contact_view(APIView): 
     
    def get(self, request):  
        donnees= ContactForm()  
        return render(request,"main/index.html",{'form':donnees})  

    def post(self, request):
        form= ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['hassanif19@gmail.com']
            if cc_myself:
               recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')

# class Index(EmailMixin, TemplateView):
#     template_name = 'main/index.html'
#     email_template_name = 'main/sendMail.html'

#     def get_context_data(self, **kwargs):
#         """
#         Método para pegar o formulário e os dados submetidos.
#         Nota - Customize a estrutura de seu email no arquivo email.html
#         """
#         context = super(Index, self).get_context_data(**kwargs)
#         form = EmailForm()
#         # data example
#         data = dict()
#         data['email_to'] = self.request.POST.get('email_to')
#         data['title'] = self.request.POST.get('title')
#         data['message'] = self.request.POST.get('message')

#         context['form'] = form
#         context['data'] = data
#         return context

#     def post(self, request, *args, **kwargs):
#         self.send_mail()
#         return HttpResponseRedirect(reverse_lazy('main:index'))			

# def home(request):
#     return render(request,'home.html')

# class Home(TemplateView):
#     template_name = 'home.html'
# def home(request):
#     return render(request,'main/home.html')


# def send_gmail(request):
#     if request.method=="POST":
#         name = request.POST.get('name')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         print(name, subject, message)

#         send_mail(
#             subject,
#             message,
#             'hassanif19@gmail.com',
            
#             fail_silently=False,
#         )

#         return HttpResponseRedirect(reverse('main/home'))
#     else:
#         return HttpResponse('Invalid request')		