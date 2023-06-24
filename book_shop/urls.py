"""book_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import *
from django.conf.urls.static import static
from django.conf import settings
router = routers.SimpleRouter()

router.register(r'genres', BookGenreViewSet)
router.register(r'books', BookViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'users', ProfileViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registration_view,name='registration'),
    path('',include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cart/add/<int:book_id>/', add_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:book_id>/', remove_cart, name='remove_from_cart'),
    path('review/like/<int:review_id>/',like_review),
    path('review/add/<int:book_id>/', add_review),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
