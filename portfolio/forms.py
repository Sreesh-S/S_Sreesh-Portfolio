from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'glass-input',
                'placeholder': 'Your Name',
                'required': True,
                'id': 'contact-name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'glass-input',
                'placeholder': 'Your Email',
                'required': True,
                'id': 'contact-email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'glass-input',
                'placeholder': 'Your Phone (Optional)',
                'id': 'contact-phone'
            }),
            'message': forms.Textarea(attrs={
                'class': 'glass-input',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True,
                'id': 'contact-message'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
