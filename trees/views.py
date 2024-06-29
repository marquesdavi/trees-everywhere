from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tree, PlantedTree
from .forms import PlantedTreeForm


class TreeListView(ListView):
    model = Tree
    template_name = "trees/tree_list.html"


class PlantedTreeDetailView(DetailView):
    model = PlantedTree
    template_name = "trees/planted_tree_detail.html"


class PlantedTreeCreateView(LoginRequiredMixin, CreateView):
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "trees/planted_tree_form.html"
    success_url = "/trees/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
