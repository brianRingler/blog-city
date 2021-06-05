from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="home_view"),
    path('register/', views.register_view, name="register_view"),
    path('login/', views.login_view, name="login_view"),
    path('profile/', views.profile_view, name="profile_view"),
    path('blog-about/', views.blog_view, name="blog_view"),
    path('blog-about/topic/<int:topic_id>/', views.blog_about_topic, name="blog_about_topic"),

    path('add-topic/', views.add_topic, name="add_topic"),
    path('blog-about/add-post/', views.add_post, name="add_post"),
    path('blog-about/add-comment/', views.add_comment, name="add_comment"),


    path('log-out/', views.log_out, name="log_out"),
    path('profile/contact-update/',views.contact_update, name='contact_update'),
    path('profile/address-update/',views.profile_update, name='profile_update'),
]