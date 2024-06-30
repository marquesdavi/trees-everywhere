from django import forms
from .models import PlantedTree


class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ["tree", "age", "account", "latitude", "longitude"]
        widgets = {
            "latitude": forms.NumberInput(attrs={"step": 0.000001}),
            "longitude": forms.NumberInput(attrs={"step": 0.000001}),
        }


