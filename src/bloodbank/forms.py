from .models import BloodCatalog
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

Bgroup = (
    ('0', 'A+'),
    ('1', 'A-'),
    ('2', 'B+'),
    ('3', 'B-'),
    ('4', 'AB+'),
    ('5', 'AB-'),
    ('6', 'O+'),
    ('7', 'O-'),
)

Nture = (
    ('0', 'Bloodcatalog'),
    ('1', 'Donor'),
    ('2', 'Receiver'),
)

class BloodCatalogCreateForm(forms.ModelForm):
    group = forms.ChoiceField(required=True,  choices=Bgroup)
    nature = forms.ChoiceField(required=True,  choices=Nture)


    class Meta:
        model = BloodCatalog
        fields = (
            "name",
            "nature",
            "contact_no",
            "Address",
            "time_from",
            "time_to",
            "date",
            "last_transaction",
            "bags",
            "group",
        )

    def save(self, commit=True):
        user = super(BloodCatalogCreateForm, self).save(commit=False)
        BloodCatalogCreateForm.group = user.group
        BloodCatalogCreateForm.nature = user.nature
        if commit:
            user.save()
        return user


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        queryset = User.objects.filter(email__iexact=email)
        if queryset.exists():
            raise forms.ValidationError("Cannot use this email. Its already registered")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(str(password1)) < 8:
            raise forms.ValidationError("Password should be at least 8 characters long")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user
