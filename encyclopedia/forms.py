from django import forms


class PageForm(forms.Form):
    title = forms.CharField(max_length=200, label="Title", 
                            widget=forms.TextInput(attrs={
                                "name": "title",
                                "class": "form-control"
                            }))
    textarea = forms.CharField(label="Content (markdown text)", 
                               widget=forms.Textarea(attrs={"name": "content",
                                                            "class": "form-control"}))
