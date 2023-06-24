from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
import json
import datetime
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

#pull потом push
class Profile(models.Model):
	userr=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	profile_pic=models.ImageField('Аватарка',default='no_pfp.jpg',upload_to='pfp')
	bio=models.TextField(null=True, blank=True)
	def __str__(self):
		return str(self.userr)
	class Meta:
		verbose_name_plural='Профили'
		verbose_name='Профиль'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(userr=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class BookGenre(models.Model):
	genre_title = models.CharField('Название жанра',max_length=200)
	def __str__(self):
		return self.genre_title
	class Meta:
		verbose_name_plural='Жанры'
		verbose_name='Жанры'

class Author(models.Model):
	name=models.CharField('Имя автора', max_length=50)
	age=models.CharField('Дата рождения',max_length=10,null=True,blank=True)
	century=models.CharField('Век',max_length=6,null=True,blank=True)
	author_bio=models.TextField('Краткая биография', max_length=500)
	nation=models.CharField('Национальность',max_length=20,null=True,blank=True)
	image=models.ImageField(default='noimage.png',upload_to='author_images')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural='Авторы'
		verbose_name='Автора'


class Book(models.Model):
	genre = models.ForeignKey(BookGenre,on_delete=models.CASCADE,null=True)
	book_author=models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
	title = models.CharField('Название книги',max_length=200)
	plot = models.TextField('Описание')
	pub_date=models.DateTimeField('Дата публикации',null=True,blank=True,default=datetime.datetime.now())
	book_cover=models.ImageField(default='No_image.png',upload_to='images')
	av=models.BooleanField(default=True)
	price=models.DecimalField(max_digits=10,decimal_places=0,null=True,blank=True)
	stock=models.PositiveIntegerField(null=True,blank=True)

	def __str__(self):
		return self.title
	class Meta:
		verbose_name_plural='Книги'
		verbose_name='Книги'
		
	
class Review(models.Model):
	book = models.ForeignKey(Book,on_delete=models.CASCADE)
	user = models.ForeignKey(Profile,null=True, on_delete=models.SET_NULL)
	revdate=models.DateTimeField('Время публикации',null=True,blank=True,default=datetime.datetime.now())
	book_review = models.TextField('Рецензия')
	rate = models.DecimalField('Оценка',validators=[MinValueValidator(1),MaxValueValidator(10)],max_digits=10, decimal_places=0,null=True)
	likes = models.ManyToManyField(Profile, related_name='liked_posts')
	def total_likes(self):
		return self.likes.count()
	def __str__(self):
		return self.book_review
	class Meta:
		verbose_name_plural='Рецензии'
		verbose_name='Рецензию'
