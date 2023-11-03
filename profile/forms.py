from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'address', 'location', 'image', 'color', 'font_preference']

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile.save()

        return profile


class FontPreferenceForm(forms.ModelForm):
    FONT_CHOICES = (
        ('Default', 'Default'),
        ('Open Sans', 'Open Sans'),
        ('Young Serif', 'Young Serif'),
        ('Roboto Slab', 'Roboto Slab'),
        ('Roboto Mono', 'Roboto Mono'),
        ('Noto Sans JP', 'Noto Sans JP'),
        ('Yuji Hentaigana Akari', 'Yuji Hentaigana Akari'),
        ('Agbalumo', 'Agbalumo'),
        ('Alegreya Sans', 'Alegreya Sans'),
        ('Montserrat', 'Montserrat'),
        ('Edu TAS Begginer', 'Edu TAS Begginer'),
        ('Playpen Sans', 'Playpen Sans'),
    )
    # Replaced the font field with choices added new font option

    # Add the font field with choices
    font_preference = forms.ChoiceField(
        choices=FONT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Profile
        fields = ['font_preference']
