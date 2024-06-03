from django import forms

class TokenForm(forms.Form):
    bot_token = forms.CharField(widget=forms.PasswordInput, label="Discord Bot Token")
