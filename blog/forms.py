from django import forms
from .models import Post, SiteConfig


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'summary', 'content', 'published']
        widgets = {
            'title':   forms.TextInput(attrs={'placeholder': 'Title'}),
            'slug':    forms.TextInput(attrs={'placeholder': 'auto-generated if empty'}),
            'summary': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short preview text...'}),
            'content': forms.Textarea(attrs={'rows': 20, 'placeholder': 'Markdown supported...'}),
        }


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = ['owner_name', 'tagline', 'about', 'avatar_image']
        widgets = {
            'owner_name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'tagline':    forms.TextInput(attrs={'placeholder': 'short line about you'}),
            'about':      forms.Textarea(attrs={'rows': 4, 'placeholder': 'A paragraph about yourself...'}),
        }
