from django import forms

class SearchPeopleForm(forms.Form):
    q = forms.CharField()
    