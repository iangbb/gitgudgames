from django import forms
from django.contrib.auth.models import User
from reviews.models import User, UserProfile, Review
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

    # Validation of password for profile edit
    def clean_password(self):
        password = self.data['password']
        password_confirm = self.data['password_confirm']
        if len(password) < 8:
            raise forms.ValidationError("Password is too short.")
        elif password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password

    @staticmethod
    def validate_username(username):
        if len(username) < 3 or len(username) > 16:
            raise forms.ValidationError("Your username must be 3-16 characters long.")

        if any(not char.isalnum() for char in username):
            raise forms.ValidationError("Your username can't contain any special characters.")

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
    # Personal
    display_name = forms.CharField(max_length=128, help_text="Display Name (Optional)", required=False)
    email = forms.EmailField(help_text="Email")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),
        input_formats=('%d/%m/%Y', ), help_text="Date of Birth")
    # Password
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm Password")
    # Extra
    profile_image = forms.ImageField(help_text="Profile Image")
    biography = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 90, 'class': 'form-control'}), help_text="Biography")
    # Hidden data
    is_journalist = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ('display_name', 'email', 'date_of_birth',
            'profile_image', 'biography', 'is_journalist')

    def clean_display_name(self):
        display_name = self.data['display_name']
        if len(display_name) > 16:
            raise forms.ValidationError("Display name is too long.")
        elif len(display_name) < 3:
            raise forms.ValidationError("Display name is too short.")
        return display_name

    def clean_date_of_birth(self):
        date_of_birth = self.data['date_of_birth']
        today = datetime.date.today()
        if date_of_birth > today:
            raise forms.ValidationError("Date is set to the future.")
        else:
            this_year_birth_date = datetime.date(today.year, date_of_birth.month, date_of_birth.day)
            if this_year_birth_date < today:
                if today.year - date_of_birth.year < 10:
                    raise forms.ValidationError("Too young.")
        return date_of_birth

    def clean_profile_image(self, file):
        print(file.name)
        if file.size > 10000000:
            raise forms.ValidationError("File is too large.")
        return file

    def clean_biography(self):
        biography = self.data['biography']
        if len(biography) > 2000:
            raise forms.ValidationError("Biography is too long.")
        return biography

class ReviewForm(forms.ModelForm):
    rating = forms.CharField(widget=forms.Select(choices=Review.RATINGS,
                                                 attrs={'class': 'form-control', 'style': 'width: 15%'}), required=True)
    review_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 90, 'class': 'form-control'}),
                                  max_length=2000, required=True)

    def __init__(self, *args, **kwargs):
        self.poster = args[1]
        self.game = args[2]
        super(ReviewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ('rating', 'review_text')
