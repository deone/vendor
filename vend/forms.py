from django import forms
from django.conf import settings

class VendForm(forms.Form):
    value = forms.ChoiceField(label='Value', choices=settings.PRICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.ChoiceField(label='Quantity', choices=settings.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self):
        pass
