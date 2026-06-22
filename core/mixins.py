from django.contrib import messages
from django.http import JsonResponse


class AjaxFormMixin:
    def _is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def ajax_success(self, message):
        messages.success(self.request, message)
        return JsonResponse({'success': True})

    def ajax_error(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    def form_invalid(self, form):
        if self._is_ajax():
            return self.ajax_error(form)
        return super().form_invalid(form)
