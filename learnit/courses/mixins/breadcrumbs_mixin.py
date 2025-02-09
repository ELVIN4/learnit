from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BreadcrumbsMixin:
    breadcrumbs = None

    def get_breadcrumbs(self):
        """
        Возвращает список крошек.
        """
        if self.breadcrumbs is not None:
            return self.breadcrumbs
        return [
            {"name": _("Home"), "url": reverse("main")},
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()

        return context
