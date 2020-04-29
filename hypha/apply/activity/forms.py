from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from pagedown.widgets import PagedownWidget

from .models import VISIBILILTY_HELP_TEXT, VISIBILITY, Activity


class CommentForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('message', 'visibility')
        labels = {
            'visibility': 'Visible to',
            'message': 'Message',
        }
        widgets = {
            'visibility': forms.MultipleChoiceField(),
            'message': PagedownWidget(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_visibility = self._meta.model.visibility_for(user)
        self.visibility_choices = self._meta.model.visibility_choices_for(user)
        self.fields['visibility'] = forms.MultipleChoiceField(choices=self.visibility_choices, widget=forms.CheckboxSelectMultiple)
        visibility = self.fields['visibility']
        # Set default visibility to "team" for staff and to "applicant" for everyone else.
        visibility.initial = self.visibility_choices[1] if user.is_apply_staff else self.visibility_choices[0]
        # visibility.choices = self.visibility_choices
        # visibility.help_text = mark_safe('<br>'.join(
        #     [VISIBILITY[choice] + ': ' + VISIBILILTY_HELP_TEXT[choice] for choice in self.allowed_visibility]
        # ))


    def clean_visibility(self):
        data = self.cleaned_data['visibility']
        choice = ' '.join(map(str, data)) 
        print("self: ", self)
        print(choice)
        if choice not in self.allowed_visibility:
            print(choice)
            raise ValidationError('You do not have permission for that visibility.')
        return choice
