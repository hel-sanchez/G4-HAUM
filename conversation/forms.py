from django import forms

from conversation.models import ConversationMessage


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'mt-2 w-full px-6 py-4 rounded-lg border border-black' 'form-control', 'rows': 3})
        }