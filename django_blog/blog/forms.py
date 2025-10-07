
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from .models import Post, Comment, Tag
from taggit.forms import TagWidget



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email",)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        label="",
        help_text="Write your comment here."
    )

    class Meta:
        model = Comment
        fields = ["content"]



class PostForm(forms.ModelForm):
    # new field for simple comma-separated tag input
    tags_input = forms.CharField(
        required=False,
        label="Tags (comma separated)",
        help_text="Add tags separated by commas, e.g. django,python,web"
    )

    class Meta:
        model = Post
        fields = ["title", "content"]  # tags handled via tags_input

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if editing, populate tags_input with existing tags
        if self.instance and self.instance.pk:
            self.fields["tags_input"].initial = ", ".join(t.name for t in self.instance.tags.all())

    def save(self, commit=True, *args, **kwargs):
        # pop tags_input before saving Post
        tags_str = self.cleaned_data.pop("tags_input", "")
        post = super().save(commit=commit, *args, **kwargs)
        if tags_str is not None:
            tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
            # create or get tags and set M2M
            tag_objs = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag_obj)
            # replace the tags for the post
            post.tags.set(tag_objs)
        return post


