from django import forms
from .widgets import CollaboratorsWidget


class CollaboratorsField(forms.CharField):
    """
    Collaborators etc etc
    """

    widget = CollaboratorsWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        collaborators = Collaborators.objects.filter(
            collaborator=self.instance
        ) # need to figure out what the relation would be called "Collaborators.objects" is placeholder

    for i in range(len(collaborators) + 1):
            field_name = 'collaborator_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = collaborators[i].collaborator
            except IndexError:
                self.initial[field_name] = “”
        # create an extra blank field
        field_name = 'collaborator_%s' % (i + 1,)
        self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        collaborators = set()
        i = 0
        field_name = 'collaborators_%s' % (i,)
        while self.cleaned_data.get(field_name):
           collaborator = self.cleaned_data[field_name]
           if collaborator in collaborators:
               self.add_error(field_name, 'Duplicate')
           else:
               collaborators.add(interest)
           i += 1
           field_name = 'collaborator_%s' % (i,)
       self.cleaned_data[“collaborators”] = collaborators
    
