from django.forms.models import BaseInlineFormSet, model_to_dict
from django.core.exceptions import ValidationError
from django import forms
from models import *

class TemplatedFormSet(BaseInlineFormSet):
	def __init__(self, *pargs, **kwargs):
		super(TemplatedFormSet, self).__init__(*pargs, **kwargs)
		self.template_form = self.empty_form
		
	def __iter__(self):
		for form in self.forms:
			yield form
		yield self.template_form
	def __len__(self):
		return super(TemplatedFormSet, self).__len__()+1
		
class MediaInlineForm(ModelForm):
	new_type = forms.ChoiceField(choices=((1, "New Medium"), (2, "Existing Medium")), required=False, widget=forms.RadioSelect, initial='1')
	index_srch = forms.IntegerField(required=False)
	loc_srch = forms.ModelChoiceField(queryset=Location.objects, required=False, initial=Location.objects.get(name='Binder A'))
	
	def __init__(self, *pargs, **kwargs):
		super(MediaInlineForm, self).__init__(*pargs, **kwargs)
		
		if self.instance.pk is not None:
			minst = self.instance.medium
			self.preexist = True
		else:
			minst = None
			self.preexist = False
		
		self.medium_form = MediumForm(instance=minst, prefix=self.prefix+"_medium")
		#self.fields["source"] = forms.ChoiceField(choices=((0, 'Existing'), (1, 'New')))
		del self.fields['medium']
	
	def save(self, *pargs, **kwargs):
		if self.cleaned_data.get('medium') == None:
			self.cleaned_data['medium'] = self.medium_form.save(commit=True)
		self.instance.medium = self.cleaned_data['medium']
		return super(MediaInlineForm, self).save(*pargs, **kwargs)
	
	def has_changed(self):
		return True #self.medium_form.has_changed() or super(MediaInlineForm, self).has_changed()
	
	def is_valid(self):
		return (self.cleaned_data.get('medium') != None or self.medium_form.is_valid()) and super(MediaInlineForm, self).is_valid()
	
	def clean(self):
		cdata = super(MediaInlineForm, self).clean()
		
		fdata = self.data
		if self.instance.pk is not None:
			minst = self.instance.medium
			#del self.fields['new_type']
		elif len(self.data) > 0:
			act = int(self.cleaned_data.get('new_type'))
			if act is 1:
				minst = None
			elif act is 2:
				fdata = None
				try:
					minst = MediaObject.objects.get(location=self.cleaned_data.get('loc_srch'), index=self.cleaned_data.get('index_srch'))
					cdata['medium'] = minst
				except:
					raise ValidationError('Could not find existing Medium matching parameters')
		else:
			minst = None
			
		self.medium_form = MediumForm(fdata, instance=minst, prefix=self.prefix+"_medium")
		return cdata

class MediumForm(ModelForm):
	class Meta:
		model=MediaObject
		
	def __init__(self, *pargs, **kwargs):
		super(MediumForm, self).__init__(*pargs, **kwargs)
		
class MovieForm(ModelForm):
	class Meta:
		model=Movie
		exclude = ['mediums']