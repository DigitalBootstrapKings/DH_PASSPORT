from rest_framework import serializers
from .models import User, Vaccinated, CovidTest, OneTimeText

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = '__all__'

class VaccinatedSerializer(serializers.ModelSerializer):
    class Meta():
        model = Vaccinated
        fields = '__all__'

class CovidTestSerializer(serializers.ModelSerializer):
    class Meta():
        model = CovidTest
        fields = '__all__'

class OneTimeTextSerializer(serializers.ModelSerializer):
    class Meta():
        model = OneTimeText
        fields = '__all__'
