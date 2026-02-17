from django import forms
from event.models import Event, Category


#Django model form 

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','event_date','participant','category','location','asset']

        widgets = {
            'name' : forms.TextInput(attrs={
                'class': "border-2 border-gray-500 w-100 rounded-lg mt-5 px-2",
                'placeholder': "Enter Event title"
            }),
            'description' : forms.TextInput(attrs={
                'class': "border-2 border-gray-500 rounded-lg h-40 mt-5 px-2",
                'placeholder': "Describe event details"
            }),
            'event_date' : forms.SelectDateWidget(attrs={
                'class': "border-2 border-gray-500 bg-gray-100 my-4 rounded-sm"
            }),
            'location' : forms.TextInput(attrs={
                'class': "border-2 border-gray-500 w-100 rounded-lg mt-5 px-2",
                'placeholder': "Event Location"
            }),
            'participant' : forms.CheckboxSelectMultiple,
        }

class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })
