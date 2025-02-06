from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ("user",)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea input-bordered w-full', 'rows': 4}),
        }