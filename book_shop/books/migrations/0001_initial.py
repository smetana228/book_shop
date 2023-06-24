# Generated by Django 4.1.6 on 2023-06-24 10:48

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя автора')),
                ('age', models.CharField(blank=True, max_length=10, null=True, verbose_name='Дата рождения')),
                ('century', models.CharField(blank=True, max_length=6, null=True, verbose_name='Век')),
                ('author_bio', models.TextField(max_length=500, verbose_name='Краткая биография')),
                ('nation', models.CharField(blank=True, max_length=20, null=True, verbose_name='Национальность')),
                ('image', models.ImageField(default='noimage.png', upload_to='author_images')),
            ],
            options={
                'verbose_name': 'Автора',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название книги')),
                ('plot', models.TextField(verbose_name='Описание')),
                ('pub_date', models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 24, 16, 48, 58, 134168), null=True, verbose_name='Дата публикации')),
                ('book_cover', models.ImageField(default='No_image.png', upload_to='images')),
                ('av', models.BooleanField(default=True)),
                ('price', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('stock', models.PositiveIntegerField(blank=True, null=True)),
                ('book_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.author')),
            ],
            options={
                'verbose_name': 'Книги',
                'verbose_name_plural': 'Книги',
            },
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_title', models.CharField(max_length=200, verbose_name='Название жанра')),
            ],
            options={
                'verbose_name': 'Жанры',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(default='no_pfp.jpg', upload_to='pfp', verbose_name='Аватарка')),
                ('bio', models.TextField(blank=True, null=True)),
                ('userr', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revdate', models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 24, 16, 48, 58, 134168), null=True, verbose_name='Время публикации')),
                ('book_review', models.TextField(verbose_name='Рецензия')),
                ('rate', models.DecimalField(decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('likes', models.ManyToManyField(related_name='liked_posts', to='books.profile')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.profile')),
            ],
            options={
                'verbose_name': 'Рецензию',
                'verbose_name_plural': 'Рецензии',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.bookgenre'),
        ),
    ]
