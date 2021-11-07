from rest_framework_mongoengine import serializers
from main.models import Adresse 

class AdresseSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Adresse
        fields = ['location']

      