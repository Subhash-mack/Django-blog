from django.contrib import admin
from .models import Profile,Message,Thread,TrackingModel
# Register your models here.
class MessageInline(admin.StackedInline):
    model = Message
    fields = ('sender', 'text')
    readonly_fields = ('sender', 'text')


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    inlines = (MessageInline,)

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message)
admin.site.register(Profile)

