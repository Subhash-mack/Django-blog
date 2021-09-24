from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from users.models import Message
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def likedby(self):
        return (" ".join([str(p) for p in self.likes.all()])).split()

class Comments(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment on {self.post.title} by {self.user.username}'


class Events(models.Model):
    title=models.CharField(max_length=200)
    start_time=models.DateTimeField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="calendar_events")

    def __str__(self):
        return f'{self.title} by {self.user.username}'

    def clean(self):
        print(self.start_time)
        if self.start_time<timezone.now():
            raise ValidationError('You can only add events for future dates')
    
    @property
    def get_html_url(self):
        url = reverse('edit-event', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class Notification(models.Model):
    Notification_type=models.IntegerField()
    to_user=models.ForeignKey(User,related_name="notification_to",on_delete=models.CASCADE,null=True)
    from_user=models.ForeignKey(User,related_name="notification_from",on_delete=models.CASCADE,null=True)
    post=models.ForeignKey('Post',on_delete=models.CASCADE,related_name="+",blank=True,null=True)
    comment=models.ForeignKey('Comments',on_delete=models.CASCADE,related_name="+",blank=True,null=True)
    message=models.ForeignKey(Message,on_delete=models.CASCADE,related_name="chat",blank=True,null=True)
    date=models.DateTimeField(default=timezone.now)
    user_has_seen=models.BooleanField(default=False)
    

    

