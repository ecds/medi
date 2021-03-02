from dal import autocomplete

from django import forms
from .models import RelatedWoman, FamilyMembership, RelatedOther

class RelatedWomanForm(forms.ModelForm):
    class Meta:
        model = RelatedWoman
        fields = ('__all__')
        widgets = {
            'related_woman': autocomplete.ModelSelect2(url='woman-autocomplete')
        }

class FamilyMembershipForm(forms.ModelForm):
    class Meta:
        model = FamilyMembership
        fields = ('__all__')
        widgets = {
            'family_member': autocomplete.ModelSelect2(url='familymember-autocomplete')
        }

class RelatedOtherForm(forms.ModelForm):
    class Meta:
        model = RelatedOther
        fields = ('__all__')
        widgets = {
            'other': autocomplete.ModelSelect2(url='relatedother-autocomplete')
        }
