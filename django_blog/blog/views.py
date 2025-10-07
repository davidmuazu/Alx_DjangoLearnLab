from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Tag
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from django.db.models import Q

# Create your views here.


def home(request):
    return render(request, "blog/base.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You are now logged in.")
            login(request, user)  # auto-login after register (optional)
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "registration/profile.html", {"form": form})



# List all posts - public
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html" 
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 10  # opt

# Show a single post - public
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

# Create a new post - authenticated users only
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post - only the author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post - only the author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        # store post_pk for later
        self.post = get_object_or_404(Post, pk=kwargs["post_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})
    
# List posts by tag
class PostsByTagListView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name")
        return Post.objects.filter(tags__name=tag_name).order_by("-published_date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_name"] = self.kwargs.get("tag_name")
        return ctx

# Search results
class PostSearchListView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return Post.objects.none()
        # search title, content, and tag names
        return Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by("-published_date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "")
        return ctx
