from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PlantedTreeForm


class TreeListView(LoginRequiredMixin, TemplateView):
    template_name = "trees/tree_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PlantedTreeForm(user=self.request.user)
        return context
