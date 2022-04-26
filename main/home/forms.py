from django import forms
from . models import shortcut, stock, weather

class shortcutForm(forms.ModelForm):
    
    class Meta:
        model = shortcut
        fields = [
            'name',
            'site_url',            
        ]

        labels = {
            "name": "",
            'site_url': '',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'shortcutForm', 'placeholder': 'Name'}),
            'site_url': forms.TextInput(attrs={'class': 'shortcutForm', 'placeholder': 'URL-address'}),
        }

class stockForm(forms.ModelForm):

    class Meta:
        model = stock
        fields = [
            'ticker'
        ]
        labels = {
            "ticker": "",
        }
        widgets = {
            'ticker': forms.TextInput(attrs={'class': 'stockForm', 'placeholder': 'Stock Ticker'}),
        }

class weatherForm(forms.ModelForm):

    class Meta:
        model = weather
        fields = [
            'city'
        ]
        labels = {
            "city": "",
        }
        widgets = {
            'city': forms.TextInput(attrs={'class': 'stockForm', 'placeholder': 'City'}),
        }
