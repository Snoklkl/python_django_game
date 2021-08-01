from django import forms

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class stockForm(forms.Form):
    #Integer field so that we get whole numbers
    stock_request = forms.IntegerField(label=False, initial=0, max_value=99, min_value=1, required=False)
    def clean_data(self):
        data = self.cleaned_data['stock_request']
        #So we don't get 0 or empty forms.
        if data < 1:
            raise ValidationError(_("Invalid amount - must be positive whole numbers."))
        return data