# Generated by Django 3.2.4 on 2021-06-05 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('display_name', models.CharField(max_length=255, null=True)),
                ('picture', models.ImageField(blank=True, default='default-img.jpg', null=True, upload_to='profile_pic')),
                ('gender', models.CharField(max_length=6, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=155)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('street_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=100, null=True)),
                ('po_box', models.IntegerField(null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('zip_code', models.CharField(max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_address', serialize=False, to='blog_app.user')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('mobile_phone', models.CharField(max_length=12, null=True, unique=True)),
                ('office_phone', models.CharField(max_length=12, null=True)),
                ('office_text', models.CharField(max_length=10, null=True)),
                ('url', models.URLField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_contact', serialize=False, to='blog_app.user')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics_user', to='blog_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_topic', to='blog_app.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_user', to='blog_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_posts', to='blog_app.post')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_topic', to='blog_app.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_user', to='blog_app.user')),
            ],
        ),
    ]
