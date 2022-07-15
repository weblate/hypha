from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from hypha.apply.funds.models import ApplicationSubmission
from hypha.apply.stream_forms.forms import StreamBaseForm
from hypha.apply.users.groups import STAFF_GROUP_NAME

from ..models.project import COMMITTED, Approval, Contract, PacketFile, Project

User = get_user_model()


class ApproveContractForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance
        if instance:
            self.fields['id'].initial = instance.id

    def clean_id(self):
        if self.has_changed():
            raise forms.ValidationError(_('Something changed before your approval please re-review'))

    def clean(self):
        if not self.instance:
            raise forms.ValidationError(_('The contract you were trying to approve has already been approved'))

        if not self.instance.is_signed:
            raise forms.ValidationError(_('You can only approve a signed contract'))

        super().clean()

    def save(self, *args, **kwargs):
        self.instance.save()
        return self.instance


class CreateProjectForm(forms.Form):
    submission = forms.ModelChoiceField(
        queryset=ApplicationSubmission.objects.filter(project__isnull=True),
        widget=forms.HiddenInput(),
    )

    def __init__(self, instance=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['submission'].initial = instance.id

    def save(self, *args, **kwargs):
        submission = self.cleaned_data['submission']
        return Project.create_from_submission(submission)


class CreateApprovalForm(forms.ModelForm):
    by = forms.ModelChoiceField(
        queryset=User.objects.approvers(),
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Approval
        fields = ('by',)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_by(self):
        by = self.cleaned_data['by']
        if by != self.user:
            raise forms.ValidationError(_('Cannot approve for a different user'))
        return by


class MixedMetaClass(type(StreamBaseForm), type(forms.ModelForm)):
    pass


class ProjectApprovalForm(StreamBaseForm, forms.ModelForm, metaclass=MixedMetaClass):
    class Meta:
        fields = [
            'title',
        ]
        model = Project
        widgets = {
            'title': forms.HiddenInput()
        }

    def __init__(self, *args, extra_fields=None, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['form_data'] = {
            key: value
            for key, value in cleaned_data.items()
            if key not in self._meta.fields
        }
        return cleaned_data

    def save(self, *args, **kwargs):
        self.instance.form_data = {
            field: self.cleaned_data[field]
            for field in self.instance.question_field_ids
            if field in self.cleaned_data
        }
        self.instance.user_has_updated_details = True
        return super().save(*args, **kwargs)


class ChangePAFStatusForm(forms.ModelForm):
    # WIP todo: need to update this on the basis if wagtail PAF's reviewers roles
    name_prefix = 'change_paf_status_form'

    class Meta:
        fields = ['status', ]
        model = Project

    def __init__(self, instance, user, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        # self.initial['comment'] = ''
        # status_field = self.fields['status']
        # user_choices = invoice_status_user_choices(user)
        # possible_status_transitions_lut = {
        #     SUBMITTED: filter_request_choices([CHANGES_REQUESTED_BY_STAFF, APPROVED_BY_STAFF, DECLINED], user_choices),
        #     RESUBMITTED: filter_request_choices([CHANGES_REQUESTED_BY_STAFF, APPROVED_BY_STAFF, DECLINED], user_choices),
        #     CHANGES_REQUESTED_BY_STAFF: filter_request_choices([DECLINED], user_choices),
        #     APPROVED_BY_STAFF: filter_request_choices(
        #         [
        #             CHANGES_REQUESTED_BY_FINANCE_1, APPROVED_BY_FINANCE_1,
        #         ],
        #         user_choices
        #     ),
        #     CHANGES_REQUESTED_BY_FINANCE_1: filter_request_choices([CHANGES_REQUESTED_BY_STAFF, DECLINED], user_choices),
        #     CHANGES_REQUESTED_BY_FINANCE_2: filter_request_choices(
        #         [
        #             CHANGES_REQUESTED_BY_FINANCE_1, APPROVED_BY_FINANCE_1,
        #         ],
        #         user_choices
        #     ),
        #     APPROVED_BY_FINANCE_1: filter_request_choices([CHANGES_REQUESTED_BY_FINANCE_2, APPROVED_BY_FINANCE_2], user_choices),
        #     APPROVED_BY_FINANCE_2: filter_request_choices([CONVERTED, PAID], user_choices),
        #     CONVERTED: filter_request_choices([PAID], user_choices),
        # }
        # status_field.choices = possible_status_transitions_lut.get(instance.status, [])

    # def clean(self):
    #     cleaned_data = super().clean()
    #     status = cleaned_data['status']
    #     if not self.instance.valid_checks and status == APPROVED_BY_FINANCE_1:
    #         self.add_error('status', _('Required checks on this invoice need to be compeleted for approval.'))
    #     return cleaned_data


class RejectionForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

    def __init__(self, instance=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RemoveDocumentForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        fields = ['id']
        model = PacketFile

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SetPendingForm(forms.ModelForm):
    class Meta:
        fields = ['id']
        model = Project
        widgets = {'id': forms.HiddenInput()}

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.instance.status != COMMITTED:
            raise forms.ValidationError(_('A Project can only be sent for Approval when Committed.'))

        if self.instance.is_locked:
            raise forms.ValidationError(_('A Project can only be sent for Approval once'))

        super().clean()

    def save(self, *args, **kwargs):
        self.instance.is_locked = True
        return super().save(*args, **kwargs)


class UploadContractForm(forms.ModelForm):
    class Meta:
        fields = ['file']
        model = Contract


class StaffUploadContractForm(forms.ModelForm):
    class Meta:
        fields = ['file', 'is_signed']
        model = Contract


class UploadDocumentForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'category', 'document']
        model = PacketFile
        widgets = {'title': forms.TextInput()}
        labels = {
            "title": _('File Name'),
        }

    def __init__(self, user=None, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UpdateProjectLeadForm(forms.ModelForm):
    class Meta:
        fields = ['lead']
        model = Project

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lead_field = self.fields['lead']
        lead_field.label = _('Update lead from {lead} to').format(lead=self.instance.lead)

        qwargs = Q(groups__name=STAFF_GROUP_NAME) | Q(is_superuser=True)
        lead_field.queryset = (lead_field.queryset.exclude(pk=self.instance.lead_id)
                                                  .filter(qwargs)
                                                  .distinct())
