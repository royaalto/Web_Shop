from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm,PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext, ugettext_lazy as _

def getGroupChoises():
    groups = Group.objects.all()
    return tuple(map(lambda u: (str(u.id), u.name), groups))

class TestForm(forms.Form):
    your_name = forms.CharField(label='User name', max_length=30)


class LoginForm(AuthenticationForm):

    #remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    email.widget.attrs.update({'class': 'form-control'})
    user_type = forms.ChoiceField(choices=getGroupChoises(),required=True, label="User type", initial='select', widget=forms.Select())
    user_type.widget.attrs.update({'class': 'form-control'})
    user_type.help_text = "Select user type."
    terms_condition = forms.BooleanField(required=True, label="I Agree terms and condition")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control'
        })
        #Update user_type choise
        self.fields['user_type'].choices = getGroupChoises()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class EditUserProfileForm(PasswordChangeForm):

    username = forms.CharField(max_length=30, label="First Name", required=False)
    username.widget.attrs.update({'class': 'form-control'})

    first_name = forms.CharField(max_length=30,label="First Name",required=False)
    first_name.widget.attrs.update({'class': 'form-control'})

    last_name = forms.CharField(max_length=30,label="Last Name",required=False)
    last_name.widget.attrs.update({'class': 'form-control'})

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    email.widget.attrs.update({'class': 'form-control'})

    # A Checkbox for change password option
    change_password = forms.BooleanField(label="Change password", required=False)


    def __init__(self,user, *args, **kwargs):

        super(EditUserProfileForm, self).__init__(user, *args, **kwargs)
        if(user):
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

            self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
            self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
            self.fields['new_password1'].required=False
            self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
            self.fields['new_password2'].required=False

            # Reorder fields not working?
            #self.fields.keyOrder = ['username','first_name','last_name', 'email', 'old_password','change_password','new_password1', 'new_password2']



    class Meta:
        # this reorder also not working?
        fields = ('username','first_name','last_name', 'email', 'old_password','change_password','new_password1', 'new_password2')

class ChooseGroupForm(forms.Form):
    user_type = forms.ChoiceField(choices=getGroupChoises(),required=True, label="User type", initial='select', widget=forms.Select())
    user_type.widget.attrs.update({'class': 'form-control'})
    user_type.help_text = "Select user type."
    def __init__(self, *args, **kwargs):
        super(ChooseGroupForm, self).__init__(*args, **kwargs)
        #Update user_type choise
        self.fields['user_type'].choices = getGroupChoises()
