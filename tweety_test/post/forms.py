
# from django import forms
# from .models import Post

# class TweetForm(forms.ModelForm):
#     image1 = forms.ImageField(required=False)
#     image2 = forms.ImageField(required=False)
#     image3 = forms.ImageField(required=False)
#     image4 = forms.ImageField(required=False)

#     class Meta:
#         model = Post
#         fields = ['text', 'image1', 'image2', 'image3', 'image4']
from django import forms
from .models import Post

class TweetForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['text', 'image']