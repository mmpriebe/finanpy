from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from categories.forms import CategoryForm
from categories.models import Category
from core.mixins import AjaxFormMixin


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(AjaxFormMixin, LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self._is_ajax():
            form.save()
            return self.ajax_success('Categoria criada com sucesso!')
        return super().form_valid(form)


class CategoryUpdateView(AjaxFormMixin, LoginRequiredMixin, UpdateView):
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if self._is_ajax():
            form.save()
            return self.ajax_success('Categoria atualizada com sucesso!')
        return super().form_valid(form)


class CategoryToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        category.is_active = not category.is_active
        category.save()
        messages.success(request, 'Status da categoria atualizado.')
        return redirect('categories:list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                'Esta categoria não pode ser excluída pois possui transações vinculadas.',
            )
            return redirect('categories:list')
