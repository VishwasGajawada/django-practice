from django import forms
from django.core import validators

#custom validator
# name = forms.CharField(validators=[check_for_z])
# def check_for_z(value):
#     if value[0].lower() != 'z':
#         raise forms.ValidationError("name should start with z")


class FormName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label = "Enter your email address again")
    text = forms.CharField(widget=forms.Textarea) 

    #all for one clean method
    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_e mail']
        if(email!=vmail):
            raise forms.ValidationError("Emails do not match")

    # botcatcher = forms.CharField(required=False,widget=forms.HiddenInput,validators=    [validators.MaxLengthValidator(0)])

    #custom validator , but instead use default validator like above
    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     #only a bot would fill invisible field also
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("GOTCHA BOT!")
    #     return botcatcher