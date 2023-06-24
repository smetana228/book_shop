from django.db import models 
from .models import *
from .serializers import *
from django_filters import rest_framework as filters

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
	pass
class BookFilter(filters.FilterSet):
	genre = CharFilterInFilter(field_name='genre__genre_title',lookup_expr='in')
	author = CharFilterInFilter(field_name='book_author__name',lookup_expr='in')
	class Meta:
		model = Book
		fields = ['genre','author']