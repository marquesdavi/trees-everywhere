from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied, ValidationError
from .models import PlantedTree, Tree
from .forms import PlantedTreeForm
from accounts.models import Account
from django.http import JsonResponse


class PlantedTreeListView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = "trees/planted_tree_list.html"
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        filter_type = self.request.GET.get("filter", "all")
        if filter_type == "mine":
            return PlantedTree.objects.filter(user=user).select_related("tree")
        else:
            accounts = user.accounts.all()
            return PlantedTree.objects.filter(account__in=accounts).select_related(
                "tree"
            )


class PlantedTreeDetailView(LoginRequiredMixin, DetailView):
    model = PlantedTree
    template_name = "trees/planted_tree_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (
            obj.user != self.request.user
            and obj.account not in self.request.user.accounts.all()
        ):
            raise PermissionDenied("You do not have permission to view this tree.")
        return obj


class PlantedTreeCreateView(LoginRequiredMixin, CreateView):
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "trees/planted_tree_form.html"
    success_url = reverse_lazy("planted_tree_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.account = form.cleaned_data["account"]

        if not form.instance.account.users.filter(id=self.request.user.id).exists():
            form.add_error(
                "account",
                ValidationError("User must be a member of the associated account."),
            )
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class PlantedTreeUpdateView(LoginRequiredMixin, UpdateView):
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "trees/planted_tree_form.html"
    success_url = reverse_lazy("planted_tree_list")

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class PlantedTreeDeleteView(LoginRequiredMixin, DeleteView):
    model = PlantedTree
    template_name = "trees/planted_tree_confirm_delete.html"
    success_url = reverse_lazy("planted_tree_list")

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)

