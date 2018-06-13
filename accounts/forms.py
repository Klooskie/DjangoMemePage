from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Incorrect login or password")

        if not user.is_active:
            raise forms.ValidationError("User deactivated")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="First name (optional)", required=False)
    last_name = forms.CharField(max_length=150, label="Last name (optional)", required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")

        return email

    def clean_password2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError("Passwords do not match")

        return password
