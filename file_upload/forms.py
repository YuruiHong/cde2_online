from django import forms
from .models import File

allowed_ext = ['txt', 'md', 'tex', 'log', 'xml', 'html', 'htm', 'pdf']


# Regular form
class FileUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    contributor = forms.CharField(
        label="Your Name", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in allowed_ext:
            raise forms.ValidationError("Only these file formats are allowed: "
                                        + ", ".join(allowed_ext) + ".")
        # return cleaned data is very important.
        return file


# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'contributor', 'description')

        widgets = {
            'contributor': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in allowed_ext:
            raise forms.ValidationError("Only these file formats are allowed: "
                                        + ", ".join(allowed_ext) + ".")
        # return cleaned data is very important.
        return file
