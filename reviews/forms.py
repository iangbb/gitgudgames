from django import forms
from reviews.models import User, UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # Override clean method to perform password confirmation checks
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        UserForm.validate_password(password, password_confirm)

        return cleaned_data

    # Method for performing password validation
    # Raises a ValidationError if any condition is not met, higher priority conditions go to the top
    @staticmethod
    def validate_password(password, confirm):
        if len(password) < 8:
            raise forms.ValidationError("Your password must be at least 8 characters long.")

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise forms.ValidationError("Your password must contain at least one letter and one number.")

        if password != confirm:
            raise forms.ValidationError("Passwords don't match.")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_image', 'date_of_birth', 'biography')
