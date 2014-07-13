from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from passwords.fields import PasswordField

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, 
        label='Email')
    group = forms.ChoiceField(required=True,
        choices=[(index, group.name) for index, group in enumerate(Group.objects.filter())],
		widget=forms.Select(attrs={'class':'form-control'}))
    password2 = PasswordField(label="Password confirmation",
        help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("username", "email", "group")

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        user_group = self.cleaned_data['group']
        group = Group.objects.get(name=Group.objects.filter()[int(user_group)])

        user.groups.add(group)
        group.user_set.add(user)

        return user

class ValidatingSetPasswordForm(SetPasswordForm):
	new_password2 = PasswordField(label="New password confirmation",
        help_text="Enter the same password as above, for verification.")
