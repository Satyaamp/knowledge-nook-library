from django import forms
from .models import SeatBooking

class SeatBookingForm(forms.ModelForm):
    class Meta:
        model = SeatBooking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SeatBookingForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['readonly'] = True  # Make amount readonly
