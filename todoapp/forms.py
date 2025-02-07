from django import forms
from .models import Category, Task

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ("user",)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea input-bordered w-full', 'rows': 4}),
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ("user", )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full mt-1'}),
            'description': forms.Textarea(attrs={'class': 'textarea input-bordered w-full mt-1', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'input input-bordered w-full mt-1'}),
            'priority': forms.Select(attrs={'class': 'input input-bordered w-full mt-1'}),
            'status': forms.Select(attrs={'class': 'input input-bordered w-full mt-1'}),
            'completed': forms.Select(attrs={'class': 'input input-bordered w-full mt-1'}),
            'due_date': forms.DateInput(attrs={'class': 'input input-bordered w-full mt-1', 'type': 'date'}),
        }

