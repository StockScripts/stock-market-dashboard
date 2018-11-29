from django import forms

from .models import Profile
from .utils import ATTRIBUTES, TIME_INTERVALS, STOCKS

class UserSettingsForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('refresh_time', )

class StockFilterForm(forms.Form):
	interval = forms.TypedChoiceField(coerce=int, choices=TIME_INTERVALS)
	stock = forms.ChoiceField(choices=STOCKS)
	attribute = forms.ChoiceField(choices=ATTRIBUTES)
