from django.contrib import admin
from .models import User, ContactInfo, Address, Post, Comment, Topic

admin.site.register(User)
admin.site.register(ContactInfo)
admin.site.register(Address)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)

