from django.urls import path

from categories.views import (
    CategoryCreateView,
    CategoryListView,
    CategoryToggleView,
    CategoryUpdateView,
)

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('nova/', CategoryCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', CategoryUpdateView.as_view(), name='update'),
    path('<int:pk>/toggle/', CategoryToggleView.as_view(), name='toggle'),
]
