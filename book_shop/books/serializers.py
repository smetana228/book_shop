from rest_framework import serializers
from .models import *
from .views import *
import json
from django.contrib.auth.models import User
from django.core.serializers import serialize


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('id','profile_pic','bio')
	def to_representation(self,instance):
		representation=super().to_representation(instance)
		representation['user_name']=instance.userr.username
		representation['email']=instance.userr.email
		return representation	

class BookGenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookGenre
		fields = '__all__'
	def to_representation(self,instance):
		representation=super().to_representation(instance)
		y=Book.objects.filter(genre__genre_title=instance.genre_title).values_list('title')
		representation['books']=y
		return representation

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ('id','title','plot','pub_date','book_cover','av','price','stock')
	def to_representation(self,instance):
		representation=super().to_representation(instance)
		if instance.stock == 0:
			instance.av = False
		if instance.stock > 0:
			instance.av = True
		representation['av'] = instance.av
		representation['author']=instance.book_author.name
		representation['genre_title']=instance.genre.genre_title

		reviews=Review.objects.filter(book__title=instance.title).values_list('book_review')
		representation['reviews']=reviews
		
		rate=Review.objects.filter(book__title=instance.title).values('rate')
		rate_num=0
		num=0
		n=0
		all_rate=0
		if not len(rate)==0:
			for x in range(len(rate)):
				rate_num=rate[x]['rate']
				num+=rate_num
				n+=1
			all_rate=round(num//n,1)
		representation['rates']=all_rate

		return representation
class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = '__all__'
	def to_representation(self,instance):
		representation=super().to_representation(instance)
		y=Book.objects.filter(book_author__name=instance.name).values_list('title')
		representation['books']=y
		return representation



class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ['revdate','book_review','likes']
	def to_representation(self,instance):
		representation=super().to_representation(instance)
		bo={
			'title':str(instance.book.title),
			'author':str(instance.book.book_author.name),
			'book_cover':str(instance.book.book_cover),
		}
		representation['book']=bo
		us={
			'user_name':str(instance.user.userr),
			'user_pfp':str(instance.user.profile_pic),
			'user_email':str(instance.user.userr.email)
		}
		liked_usernames = instance.likes.values_list('userr__username', flat=True)
		representation['likes'] = liked_usernames
		representation['user']=us
		representation['total_likes']=instance.total_likes()
		return representation