from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import JobApplication


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = (
            "company",
            "job_role",
            "application_date",
            "status",
            "job_url",
            "notes",
        )
        widgets = {
            "application_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
