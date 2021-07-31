from django import forms

class TicketCreateForm(forms.Form):
	title = forms.CharField(label="Titre")
	description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
	image = forms.ImageField(required=False)

	title.widget.attrs.update({'class': 'form-control'})
	image.widget.attrs.update({'class': 'form-control'})

class ReviewForm(forms.Form):
	headline = forms.CharField(label="Titre")
	rating = forms.ChoiceField(label="Note", widget=forms.RadioSelect, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
	body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={'class': 'form-control'}))

	headline.widget.attrs.update({'class': 'form-control'})
	rating.widget.attrs.update({'class': 'form-check-input'})