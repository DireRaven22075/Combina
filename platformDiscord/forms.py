from django import forms

class TokenForm(forms.Form): # 디스코드 봇 토큰 설정 폼
    bot_token = forms.CharField(widget=forms.PasswordInput, label="")
