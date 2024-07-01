from django import forms
from .models import PlantedTree
from accounts.models import Account


class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ["tree", "age", "account", "latitude", "longitude"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PlantedTreeForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = Account.objects.filter(users=user)
