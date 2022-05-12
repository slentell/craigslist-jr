from django.shortcuts import render, redirect
from .models import Category, Posts
from .forms import CategoryForm, PostForm
import os
api_key = os.environ.get('SECRET_KEY')



# Create your views here.
def get_category(category_id):
    return Category.objects.get(id=category_id)

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'categories_list.html', {'categories': categories})

def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('categories_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def edit_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category_detail', category_id=category.id)

def category_detail(request, category_id):
    category = get_category(category_id)
    posts = Posts.objects.filter(category=category)
    data = {
        'category': category,
        'posts': posts,       
    }
    return render(request, 'category_detail.html', data)

def delete_category(request, category_id):
    category = get_category(category_id)
    category.delete()
    return redirect('categories_list')

def get_post(post_id):
    return Posts.objects.get(slug=post_id)


def post_detail(request, category_id, post_id):
    category = get_category(category_id)
    post = get_post(post_id)
    location_for_google = _generate_google_address(post.location)
    data = {
        'category': category,
        'post': post,
        'location': location_for_google
    }
    return render(request, 'post_detail.html', data)

def _generate_google_address(location):
    modified_location = location.replace(',', '%20')
    
    
    return f'https://www.google.com/maps/embed/v1/place?q={modified_location}&key={api_key}'

def new_post(request, category_id):
    category = get_category(category_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.save()
            return redirect('category_detail', category_id=category.id)
        else:
            return render(request, 'post_form.html', {'form': form, 'category': category})
    else:
        form = PostForm()
        return render(request, 'post_form.html', {'form': form, 'category': category})

def edit_post(request, category_id, post_id):
    category = get_category(category_id)
    post = get_post(post_id)
    if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', category_id=category.id)
    else:
            form = PostForm(instance=post)
            data = {'form': form, 'category': category}
            return render(request, 'post_form.html', data)
        

def delete_post(request, category_id, post_id):
    post = get_post(post_id)
    post.delete()
    return redirect('category_detail', category_id)


