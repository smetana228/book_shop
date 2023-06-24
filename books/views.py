from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .services import BookFilter
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from validate_email import validate_email
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

User = get_user_model()

def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Проверка наличия обязательных полей
        if not username or not password or not email:
            return JsonResponse({'error': 'Не заполнены все обязательные поля.'})

        # Проверка существования пользователя с таким же именем
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Пользователь с таким именем уже существует.'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Пользователь с такой почтой уже существует.'})
        if not validate_email(email):
            return JsonResponse({'error': 'Такой почты не существует.'})

        # Создание пользователя
        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'success': 'Регистрация прошла успешно.'})
    else:
        return JsonResponse({'error': 'Неверный метод запроса.'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Проверка наличия обязательных полей
        if not username or not password:
            return JsonResponse({'error': 'Не заполнены все обязательные поля.'})

        # Попытка аутентификации пользователя
        user = authenticate(request, username=username, password=password,email=email)

        # Проверка успешной аутентификации
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Авторизация прошла успешно.'})
        else:
            return JsonResponse({'error': 'Неверные учетные данные.'})

    else:
        return JsonResponse({'error': 'Неверный метод запроса.'})

def logout_view(request):
    logout(request)
    return JsonResponse({'success': 'Вы успешно вышли из системы.'})


def add_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart = request.session.get('cart', {})
    cart[str(book.id)] = {
        'name': book.title,
        'price': int(book.price)
    }
    request.session['cart'] = cart
    return JsonResponse({'status': 'success'})

def view_cart(request):
    cart = request.session.get('cart')
    return JsonResponse({'cart': cart})

def remove_cart(request, book_id):
    cart = request.session.get('cart', {})
    if str(book_id) in cart:
        del cart[str(book_id)]
        request.session['cart'] = cart
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def like_review(request, review_id):
    review = Review.objects.get(id=review_id)
    user = Profile.objects.get(userr=request.user)

    if user in review.likes.all():
        review.likes.remove(user)
        liked = False
    else:
        review.likes.add(user)
        liked = True
    data = {
        'liked': liked,
        'total_likes': review.total_likes()
    }
    return JsonResponse(data)


@login_required
def add_review(request,book_id):
    book_review = request.POST.get('book_review')
    rate=request.POST.get('rate')
    userr = Profile.objects.get(userr=request.user)
    book = Book.objects.get(id=book_id)
    review = Review.objects.create(user=userr)
    review.book.add(book)
    review.book_review.add(b_review)
    review.rate.add(r)





class BookGenreViewSet(viewsets.ModelViewSet):
	queryset=BookGenre.objects.all()
	serializer_class=BookGenreSerializer
	
class AuthorViewSet(viewsets.ModelViewSet):
	queryset=Author.objects.all()
	serializer_class=AuthorSerializer

class ProfileViewSet(viewsets.ModelViewSet):
	queryset=Profile.objects.all()
	serializer_class=ProfileSerializer

class BookViewSet(viewsets.ModelViewSet):
	queryset=Book.objects.all()
	serializer_class=BookSerializer	
	filter_backends=(DjangoFilterBackend,)
	filterset_class=BookFilter
	
class ReviewViewSet(viewsets.ModelViewSet):
	queryset=Review.objects.all()
	serializer_class=ReviewSerializer	
