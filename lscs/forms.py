from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, 
        label='Email')
    group = forms.ChoiceField(required=True,
        # ("1", "Manager"), ("2", "Surveyor")
        choices=[ (index, group.name) for index, group in enumerate(Group.objects.filter())])

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

        return user

