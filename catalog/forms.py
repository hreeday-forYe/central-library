from django import forms
import datetime
from django.core.exceptions import ValidationError 
from django.utils.translation import gettext_lazy, gettext_noop, gettext 
from .models import BookInstance

class RenewBookModelForm(forms.ModelForm):

  renewal_date = forms.DateField(
    widget= forms.DateInput(attrs={'type':'date'}),
    help_text="Select a renewal date"
  )
  def clean_renewal_date(self):
    dateData = self.cleaned_data['renewal_date']
    if dateData <= datetime.date.today():
      raise ValidationError(gettext("Invalid date entered: Date is in the past"))
    if dateData <= datetime.date.today() + datetime.timedelta(weeks=2):
      raise ValidationError(gettext("Invalid date please choose time after 2 weeks"))
    return dateData
  class Meta:
    model = BookInstance
    fields = ['renewal_date']
    labels = {"renewal_date": "Renewal Date" }
    help_texts = {"renewal_date":"Enter the new Date you want to renew of the book (today - 2 weeks)"}