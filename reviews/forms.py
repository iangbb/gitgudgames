from django import forms
from reviews.models import User, UserProfile, Review
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    #email = forms.EmailField(required=True)
    #password = forms.CharField(widget=forms.PasswordInput())
    #password_confirm = forms.CharField(widget=forms.PasswordInput())

    username = forms.CharField(max_length=128, help_text="Username", required=True)
    first_name = forms.CharField(max_length=128, help_text="First Name (Optional)", required=False)
    last_name = forms.CharField(max_length=128, help_text="Last Name (Optional)", required=False)
    email = forms.EmailField(help_text="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm Password")

    class Meta:
        model = User
        #fields = ('username', 'email', 'password')
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

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
    # User-editable data
    date_of_birth = forms.DateField(False, False, help_text="Date of Birth")
    profile_image = forms.ImageField(help_text="Profile Image")
    biography = forms.CharField(max_length=2000, help_text="Biography")

    # Hidden data
    is_journalist = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ('profile_image', 'date_of_birth', 'biography', 'is_journalist')


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
