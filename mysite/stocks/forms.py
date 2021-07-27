from django import forms

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class stockForm(forms.Form):
    stock_request = forms.IntegerField(label="stock_request")

    def clean_data(self):
        data = self.clean_data['stock_request']

        if data < 1:
            raise ValidationError(_("Invalid amount - must be positive whole numbers."))

        return data