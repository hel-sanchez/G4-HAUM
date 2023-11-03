from django.contrib.auth.forms import UserChangeForm
from profile.models import Profile


class EditUserForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'bio',
            'location',
            'address',
        )