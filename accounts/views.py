from django.views.generic import TemplateView
from .models import Account
from .forms import AccountForm
from django.contrib.auth.mixins import LoginRequiredMixin


class AccountTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/account_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AccountForm()
        context["object_list"] = Account.objects.all()
        return context
