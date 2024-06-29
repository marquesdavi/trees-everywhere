from django import forms
from .models import PlantedTree


class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ["tree", "age", "account", "latitude", "longitude"]
