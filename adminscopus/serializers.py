from rest_framework import serializers
from adminscopus.models import *

class ProyectoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScpProyecto
		fields = ("nombre","descripcion","register","apikey","tipo")