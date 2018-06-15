from django import forms

class QueueForm(forms.Form):
    # max len of mc username is 16 characters
    username = forms.CharField(label="username", max_length=20) 
    email = forms.EmailField()
    password = forms.CharField(label="password",
                                widget=forms.PasswordInput)
