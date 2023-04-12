from django import forms
from .models import Contact, Comment, OnlineForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import PrependedText

class OnlineFormToFill(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(OnlineFormToFill,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-contactForm'
        self.helper.form_method = 'post'
        self.helper.form_class = 'blueForms'
        self.helper.form_action = 'emsite:online_form'
        #self.helper.add_input(Submit('submit','Submit'))
        self.helper.layout = Layout(
            Fieldset(
                    'Fill in details',
                    'name',
                    'course_name',
                    'phonenum',
                    'email',
                    'state',
                    'country',
                    'prof_creds',
                    'proposed_info'
                    ),
            ButtonHolder(
                    Submit('submit','Submit')
            ),
        )
            
    class Meta:
        model = OnlineForm
        fields = ['name','course_name','phonenum','email','state','country','prof_creds','proposed_info']
        #labels = {'name':'Name (surname first)','course_name':'Course Name','phonenum':'Phone Number','email':'Email address','state':'State','country':'Country','prof_creds':'International Professional Credentials (if any)','proposed_info':'Information you will propose'}
    
class ContactForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ContactForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-contactForm'
        self.helper.form_method = 'post'
        self.helper.form_class = 'blueForms'
        self.helper.form_action = 'emsite:contact'
        self.helper.add_input(Submit('submit','Submit'))
    class Meta:
        model = Contact
        fields = ['name','email','phone_number','message']

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')