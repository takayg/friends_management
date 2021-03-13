from django import forms
from .models import Event, Friend
import datetime

class EventForm(forms.ModelForm):
    """ Form for Event """
    
    class Meta:
        model = Event
        fields = ('event_name', 'place', 'memo')
 
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class DateForm(forms.Form):
    date_now = datetime.datetime.now()
    years = tuple([(x, str(x)) for x in range(1990, 2030)])
    year = forms.ChoiceField(choices=years, initial=date_now.year)
    months = tuple([(x, str(x)) for x in range(1, 13)])
    month = forms.ChoiceField(choices=months, initial=date_now.month)




        

