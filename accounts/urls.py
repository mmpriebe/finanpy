from django.urls import path

from accounts.views import (
    AccountCreateView,
    AccountDeleteView,
    AccountListView,
    AccountToggleView,
    AccountUpdateView,
)

app_name = 'accounts'

urlpatterns = [
    path('', AccountListView.as_view(), name='list'),
    path('nova/', AccountCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', AccountUpdateView.as_view(), name='update'),
    path('<int:pk>/toggle/', AccountToggleView.as_view(), name='toggle'),
    path('<int:pk>/excluir/', AccountDeleteView.as_view(), name='delete'),
]
