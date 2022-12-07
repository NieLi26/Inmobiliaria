from django import forms
from . models import NewsletterUser

class NewsletterUserForm(forms.ModelForm):
    

    class Meta:
        model = NewsletterUser
        fields = ('email',)
