from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# sample dictionary to test how to pass data to templates
# posts=[
#     {
#         'author':'Yashi',
#         'title':'Blog post 1',
#         'content':'This is the first post',
#         'date_posted':'4th July,2021'
#     },
#     {
#         'author':'Jane Doe',
#         'title':'Blog post 2',
#         'content':'This is the second post',
#         'date_posted':'4th July,2021'
#     }
# ]

posts=Post.objects.all()


def home(request):
    context={
        'posts':posts,
        'title':'Blog Home'
    } #dictionary to encapsulate the entire data
    # return render(request,'blog/home.html') this is used when static pages are loaded with no data
    return render(request,'blog/home.html',context) #when data is being passed

def about(request):
    return render(request,'blog/about.html')


class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']


class PostDetailView(DetailView):
    model=Post

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False
    

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False
    