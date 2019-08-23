from django import forms
from django.contrib.auth.models import User

from .models import Profile
import re


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bio')


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Your current password was entered incorrectly.')
        return current_password

    def clean_new_password(self):
        current_password = self.cleaned_data.get('current_password')
        new_password = self.cleaned_data.get('new_password')

        errors = []
        if current_password is not None and current_password == new_password:
            errors.append('Password must not be the same as the current password.')
        if len(new_password) < 14:
            errors.append('Minimum password length of 14 characters.')
        if re.search(r'[A-Z]', new_password) is None or re.search(r'[a-z]', new_password) is None:
            errors.append('Password must use of both uppercase and lowercase letters.')
        if re.search(r'[0-9]', new_password) is None:
            errors.append('Password must include of one or more numerical digits.')
        if re.search('[@_!#$%^&*()<>?/\|}{~:]', new_password) is None:
            errors.append('Password must include of special characters, such as @, #, $.')
        if self.user.first_name in new_password or self.user.last_name in new_password:
            errors.append(
                'Password cannot contain the username or parts of the user’s full name, such as his first name.'
            )

        if errors:
            raise forms.ValidationError(errors)
        return new_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password is not None and new_password != confirm_password:
            raise forms.ValidationError('Please enter same password as new password.')
        return confirm_password
