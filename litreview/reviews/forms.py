from django import forms

class TicketCreateForm(forms.Form):
	title = forms.CharField(label="Titre")
	description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
	image = forms.ImageField()

	title.widget.attrs.update({'class': 'form-control'})
	image.widget.attrs.update({'class': 'form-control'})