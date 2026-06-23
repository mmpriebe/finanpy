from django.urls import path

from profiles.views import PasswordChangeView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('perfil/', ProfileDetailView.as_view(), name='profile-detail'),
    path('perfil/editar/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('perfil/senha/', PasswordChangeView.as_view(), name='password-change'),
]
