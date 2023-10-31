from django import forms

from profile.models import Location
from .models import Item, Category

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border-gray-950 border-2 focus:outline-none focus:border-gray-950'


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'price', 'description', 'image']
        widgets = {
            'category': forms.Select(choices=Category.objects.all(), attrs={'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')

        if not image:
            self.add_error('image', "Please upload an image.")


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','is_sold', 'price', 'description', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }


class addCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Adjust to include the fields you want to edit


class addLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
