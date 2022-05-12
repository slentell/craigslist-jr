from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Category, Posts

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cat_name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'description', 'price', 'location','seller','image']
        exclude = ['category','date_listed']

    
