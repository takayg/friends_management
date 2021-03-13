from django import forms
from .models import Friend
import datetime

class FriendForm(forms.ModelForm):
    """ Form for Friend """
   
    class Meta:
        model = Friend
        fields = ('friend_name', 'birth_day', 'memo', 'photo')
        widgets = {
            'birth_day': forms.SelectDateWidget(years=[x for x in range(1900, datetime.datetime.now().year + 1)])
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values(attrs={"type":"date"}):
                field.widget.attrs['class'] = 'form-control'
