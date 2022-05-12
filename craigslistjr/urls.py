from django.urls import path
from . import views

urlpatterns = [
    path('', views.categories_list, name='categories_list'),
    path('new', views.new_category, name='new'),
    path('<uuid:category_id>', views.category_detail, name='category_detail'),
    path('<uuid:category_id>/edit', views.edit_category, name='edit_category'),
    path('<uuid:category_id>/delete', views.delete_category, name='delete_category'),
    
    
    path('<uuid:category_id>/posts/new', views.new_post, name='new_post'),
    path('<uuid:category_id>/posts/<slug:post_id>/', views.post_detail, name='post_detail' ),
    path('<uuid:category_id>/posts/<slug:post_id>/edit', views.edit_post, name='edit_post'),
    path('<uuid:category_id>/posts/<slug:post_id>/delete', views.delete_post, name='delete_post'),

]