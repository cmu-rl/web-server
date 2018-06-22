from django import forms

class SignupForm(forms.Form):
    # max len of mc username is 16 characters
    username = forms.CharField(label="username", max_length=20) 
    email = forms.EmailField()
    password = forms.CharField(label="password",
                                widget=forms.PasswordInput)
    repwd = forms.CharField(label="repwd",
                                widget=forms.PasswordInput)
