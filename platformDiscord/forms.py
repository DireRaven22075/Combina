from django import forms

class TokenForm(forms.Form):
    """
    디스코드 봇 토큰 설정을 위한 폼 클래스
    - 사용자가 입력한 디스코드 봇 토큰을 안전하게 받기 위해 사용
    """
    bot_token = forms.CharField(
        widget=forms.PasswordInput,  # 비밀번호 입력 필드처럼 보여지도록 설정
        label=""  # 라벨을 빈 문자열로 설정하여 폼 필드에 라벨이 표시되지 않도록 함
    )
