from django import forms
import datetime
from .models import Event, Friend

""" Form for Event """
class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ('event_name', 'place', 'memo')
 
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

""" Form for Selecting Year and Date """
class DateForm(forms.Form):

    date_now = datetime.datetime.now() # today's information

    # select year from [1990, 2030)
    years = tuple([(x, str(x)) for x in range(1990, 2030)]) 
    year = forms.ChoiceField(choices=years, initial=date_now.year)

    # select date from [1, 12]
    months = tuple([(x, str(x)) for x in range(1, 13)]) 
    month = forms.ChoiceField(choices=months, initial=date_now.month)




        

