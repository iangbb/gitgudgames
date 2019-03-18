from django import forms
from django.contrib.auth.models import User
from reviews.models import User, UserProfile, Review
from gitgudgames.settings import DATE_INPUT_FORMATS
import datetime
import os

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=128, help_text="Username", required=True)
    email = forms.EmailField(help_text="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm Password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # Override clean method to perform password confirmation checks
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        UserForm.validate_username(username)
        UserForm.validate_password(password, password_confirm)

        return cleaned_data

    @staticmethod
    def validate_username(username):
        if username is None:
            raise forms.ValidationError("You need a username.")
        else:
            if len(username) < 3 or len(username) > 16:
                raise forms.ValidationError("Your username must be 3-16 characters long.")
            if any(not char.isalnum() for char in username):
                raise forms.ValidationError("Your username can't contain any special characters.")

    # Method for performing password validation
    # Raises a ValidationError if any condition is not met, higher priority conditions go to the top
    @staticmethod
    def validate_password(password, confirm):
        if None in (password, confirm):
            raise forms.ValidationError("You need a password.")
        else:
            if len(password) < 8:
                raise forms.ValidationError("Your password must be at least 8 characters long.")
            if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
                raise forms.ValidationError("Your password must contain at least one letter and one number.")
            if password != confirm:
                raise forms.ValidationError("Passwords don't match.")

class UserProfileForm(forms.ModelForm):
    display_name = forms.CharField(max_length=16, help_text="Display Name (Optional)", required=False)
    date_of_birth = forms.DateField(input_formats=DATE_INPUT_FORMATS, help_text="Date of Birth")
    profile_image = forms.ImageField(help_text="Profile Image")
    biography = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 90, 'class': 'form-control'}), help_text="Biography")
    is_journalist = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ('display_name', 'profile_image',
            'date_of_birth', 'biography', 'is_journalist')

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        profile_image = cleaned_data.get('profile_image')
        biography = cleaned_data.get('biography')

        UserProfileForm.validate_profile_image(profile_image)
        UserProfileForm.validate_biography(biography)

        return cleaned_data

    @staticmethod
    def validate_profile_image(profile_image):
        if profile_image is None:
            print("Profile image empty.")
            pass
        elif profile_image.size > 1000000:
            print("Profile image invalid.")
            raise forms.ValidationError("Your profile image is too big.")
        print("Profile image valid.")

    @staticmethod
    def validate_biography(biography):
        if biography is None:
            print("Biography empty.")
            pass
        elif len(biography) > 2000:
            print("Biography invalid.")
            raise forms.ValidationError("Your biography is too long.")
        print("Biography valid.")


class DetailsForm(forms.ModelForm):
    display_name = forms.CharField(max_length=16, help_text="Display Name (Optional)", required=False)
    email = forms.EmailField(help_text="Email")
    date_of_birth = forms.DateField(input_formats=DATE_INPUT_FORMATS,
        help_text="Date of Birth")

    class Meta:
        model = UserProfile
        fields = ('display_name', 'email', 'date_of_birth', )
        widgets = {
            'date_of_birth': forms.DateInput(format=DATE_INPUT_FORMATS,
                attrs={'class': 'datepicker-input', 'placeholder': 'dd/mm/yy'})
        }

    def clean(self):
        cleaned_data = super(DetailsForm, self).clean()
        display_name = cleaned_data.get('display_name')
        date_of_birth = cleaned_data.get('date_of_birth')

        print("Validating.")
        DetailsForm.validate_display_name(display_name)
        DetailsForm.validate_date_of_birth(date_of_birth)
        print("Validation done.")

        return cleaned_data

    @staticmethod
    def validate_display_name(display_name):
        if display_name is not None:
            if len(display_name) > 16:
                raise forms.ValidationError("Your display name is too long.")

    @staticmethod
    def validate_date_of_birth(date_of_birth):
        print(str(date_of_birth))
        if date_of_birth is not None:
            today = datetime.date.today()
            print(str(today))
            print(str(date_of_birth.year) + ">" + str(today.year) + ": ")
            print(str(date_of_birth.year > today.year))
            if date_of_birth.year > today.year:
                raise forms.ValidationError("Date of birth is set in the future.")


# Form for changing password
class PasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm Password")

    class Meta:
        model = User
        fields = ('password',)

    # Override clean method to perform password confirmation checks
    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        PasswordForm.validate_password(password, password_confirm)
        return cleaned_data

    # Method for performing password validation
    # Raises a ValidationError if any condition is not met, higher priority conditions go to the top
    @staticmethod
    def validate_password(password, confirm):
        if None in (password, confirm):
            raise forms.ValidationError("You need a password.")
        else:
            if len(password) < 8:
                raise forms.ValidationError("Your password must be at least 8 characters long.")
            if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
                raise forms.ValidationError("Your password must contain at least one letter and one number.")
            if password != confirm:
                raise forms.ValidationError("Passwords don't match.")





class ReviewForm(forms.ModelForm):
    rating = forms.CharField(widget=forms.Select(choices=Review.RATINGS,
                                                 attrs={'class': 'form-control', 'style': 'width: 15%'}), required=True)
    review_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 90, 'class': 'form-control'}),
                                  max_length=2000, required=True)

    class Meta:
        model = Review
        fields = ('rating', 'review_text')
