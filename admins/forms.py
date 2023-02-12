from .models import Articles, Languages, TranlsationGroups, Translations, StaticInformation
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from main.models import Applications



class LngForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название...'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Код'
            }),
            "icon": forms.FileInput(attrs={
                "class": "blog_cover_input"
            }),
            "active": forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            "default": forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }



class StaticInfForm(forms.ModelForm):
    class Meta:
        model = StaticInformation
        exclude = ['title', 'deskription', 'about_us', 'adres', 'work_time']

        widgets = {
            'email': forms.EmailInput(attrs={
                "class": "form-control",
                'placeholder': 'example@gmail.com'
            }),
            'telegram': forms.URLInput(attrs={
                "class": 'form-control',
                'placeholder': 'Telegram url'
            }),
            'instagram': forms.URLInput(attrs={
                "class": 'form-control',
                'placeholder': 'Instagram url'
            }),
            'facebook': forms.URLInput(attrs={
                "class": 'form-control',
                'placeholder': 'Facebook url'
            }),
            'youtube': forms.URLInput(attrs={
                "class": 'form-control',
                'placeholder': 'Youtube url'
            }),
            'nbm': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder' : "+998(__)_______"
            }),
            'map': forms.Textarea(attrs={
                'class': 'form-control',
            })
        }
        

class UserForm(UserCreationForm):
    password1 = forms.PasswordInput(attrs={
        'max': '6'
    })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                ('Passwords don\'t match.'), code='Invalid')
        return cd['password2']


# application form
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = '__all__'

        widgets = {
            'vehicle': forms.Select(attrs={
                "class": "form-select mb-3",
                'data-choices': '',
            }),
            'tarif': forms.Select(attrs={
                "class": "form-select mb-3",
            }),
            'ship_type': forms.Select(attrs={
                "class": "form-select mb-3",
            }),
            'status': forms.Select(attrs={
                "class": "form-select mb-3",
            }),
            'ship_via_id': forms.Select(attrs={
                "class": "form-select mb-3",
            }),
            'vehicle_runs': forms.Select(attrs={
                "class": "form-select mb-3",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            "adres_type": forms.Select(attrs={
                "class": "form-select mb-3",
            }),
        }