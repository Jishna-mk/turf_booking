from django.forms import ModelForm
from django.forms import TextInput,Textarea,NumberInput,DateInput
from .models import ManagerProfile

class ManagerProfileForm(ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ["Address","Qualification","Phone_Number","Designation","Profile_Image"]

        widgets = {
            'Phone_Number': TextInput(attrs={"class":"form-control","placeholder":"Enter Phone number"}),
            'Designation': TextInput(attrs={"class":"form-control","placeholder":"Enter  Your Designation"}),
            'Address': Textarea(attrs={"class":"form-control","placeholder":"Enter  Address"}),
            'Qualification': Textarea(attrs={"class":"form-control","placeholder":"Enter  Your Educational Qualification"}),
        }


from django import forms
from .models import TurfList

class TurfDetailsForm(forms.ModelForm):
    class Meta:
        model = TurfList  
        fields = '__all__'

