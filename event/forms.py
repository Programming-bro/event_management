from django import forms
from event.models import Event, Participant, Category

#Django form

# class TaskForm(forms.Form):
#     title = forms.CharField(max_length=250, label="Task Title")
#     description = forms.CharField(widget=forms.Textarea, label="Task Description")
#     due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
#     assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[])

#     def __init__(self,*args,**kwargs):
#         # print(args,kwargs)
#         employees = kwargs.pop("employees",[])
#         super().__init__(*args,**kwargs)
#         self.fields['assigned_to'].choices = [(emp.id,emp.name) for emp in employees]

#Django model form 

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','event_date','attended','category','location']

        widgets = {
            'name' : forms.TextInput(attrs={
                'class': "border-2 border-gray-500 w-100 rounded-lg mt-5 px-2",
                'placeholder': "Enter Event title"
            }),
            'description' : forms.TextInput(attrs={
                'class': "border-2 border-gray-500 rounded-lg h-500 mt-5 px-2",
                'placeholder': "Describe event details"
            }),
            'event_date' : forms.SelectDateWidget,
            'location' : forms.TextInput(attrs={
                'class': "border-2 border-gray-500 w-100 rounded-lg mt-5 px-2",
                'placeholder': "Event Location"
            }),
            'attended' : forms.CheckboxSelectMultiple,
            # 'category' : forms.CheckboxSelectMultiple
        }