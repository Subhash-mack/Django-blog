from django.contrib import admin
from .models import Post,Comments,Events,Notification
# Register your models here.

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Events)
admin.site.register(Notification)


