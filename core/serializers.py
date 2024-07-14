from rest_framework import serializers
from .models import *

#se usa para transformar datos python a json y viceversa
class PeriodistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodista
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class NoticiaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only= True)
    periodista = PeriodistaSerializer(read_only= True)

    class Meta:
        model = Noticia
        fields = '__all__'

