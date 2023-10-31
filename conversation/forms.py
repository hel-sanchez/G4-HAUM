from django import forms

from conversation.models import ConversationMessage


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full px-6 py-4 rounded-xl border' 'form-control', 'rows': 3})
        }