from django import forms

class ComposerForm(forms.Form):
    name = forms.CharField(max_length=255)
    birth_date = forms.DateField(required=False)
    death_date = forms.DateField(required=False)
    picture = forms.ImageField(required=False)

    def validate_date(self, birth, death): return birth < death 

class CorpusForm(forms.Form):
	title = forms.CharField(max_length=255)
	comment = forms.CharField(widget=forms.Textarea, required=False)
	picture = forms.ImageField(required=False)


class TagForm(forms.Form):
	name = forms.CharField(max_length=255)
	description = forms.CharField(widget=forms.Textarea, required=False)

class AttachmentForm(forms.Form):
    attachment = forms.FileField()
    description = forms.CharField(max_length=255, required=False)
    #uploader = models.ForeignKey(User, blank=True, null=True)

# movement should be associated with a piece..? 