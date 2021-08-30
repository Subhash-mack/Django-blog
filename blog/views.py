from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,Comments,Events
from django.db.models import Q
from .forms import CommentForm,EventForm
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import date,datetime,timedelta
import calendar
from django.contrib.auth.decorators import login_required



class CalendarView(ListView):
    model=Events
    template_name='blog/calendar.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month,self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request,id=None):
    if id:
        instance=get_object_or_404(Events,pk=id)
    else:
        instance=Events()
    form=EventForm(request.POST or None,instance=instance)
    if request.POST and form.is_valid():
        title=form.cleaned_data.get('title')
        stime=form.cleaned_data.get('start_time')
        form=Events.objects.create(title=title,start_time=stime,user=request.user)
        form.save()
        return render(request,'blog/calendar.html')
    return render(request,'blog/event.html',{'form':form})

def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

class LatestPostsView(ListView):
    model=Post
    template_name='blog/latest_posts.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5    

class UserPostListView(ListView):
    model=Post
    template_name='blog/users_post.html'
    context_object_name='posts'
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
class PostDetailView(DetailView):
    model=Post
    is_liked=False
                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        comments=Comments.objects.filter(post=post.id).order_by("-pk")
        if post.likes.filter(id=self.request.user.id).exists():
            context['is_liked'] = True
        context['total_likes']=post.total_likes()
        cf=CommentForm()
        context['comment_form']=cf
        context['comments']=comments
        return context

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url="/"
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class SearchView(ListView):
    model = Post
    template_name = 'blog/search.html'
    # context_object_name = 'all_search_results'

    def get_queryset(self):
    #    result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('q')
        print(query)
        if query:
            postresult = Post.objects.filter(Q(title__icontains=query) | Q(content=query))
            result=postresult
        else:
            result=None
        return result

def like_post(request):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    is_liked=True
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
    data={
        'value':is_liked,
        'likes':post.likes.all().count()
    }
    # return HttpResponseRedirect(post.get_absolute_url())
    return JsonResponse(data,safe=False)

def comment_post(request):
    post=get_object_or_404(Post,id=request.POST.get('commentid'))
    if request.method == 'POST':
        cf=CommentForm(request.POST or None)
        if cf.is_valid():
            content=request.POST.get('content')
            comment=Comments.objects.create(post=post,user=request.user,content=content)
            comment.save()
            return redirect(post.get_absolute_url())

def deletecomment(request,id):
    comment=get_object_or_404(Comments,id=id)
    comment.delete()
    messages.success(request,f'Comment deleted!')
    return redirect(comment.post.get_absolute_url())


def about(request):
    return render(request,'blog/about.html',{'title':'Blog About'})
