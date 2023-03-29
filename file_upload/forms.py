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
        fields = ('file', 'contributor', 'description', 'attributes')

        widgets = {
            'contributor': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
# use choice in 'Compound', 'Apparatus', 'UvvisPeak', 'UvvisSpectrum', 'IrPeak', 'IrSpectrum', 'NmrPeak', 'NmrSpectrum', 'MeltingPoint', 'GlassTransition', 'QuantumYield', 'FluorescenceLifetime', 'ElectrochemicalPotential', 'NeelTemperature', 'CurieTemperature', 'InteratomicDistance', 'CoordinationNumber', 'CNLabel'
            'attributes': forms.SelectMultiple(attrs={'class': 'form-control'},
                choices=(('MeltingPoint', 'MeltingPoint'), ('Compound', 'Compound'), ('Apparatus', 'Apparatus'), ('UvvisPeak', 'UvvisPeak'), ('UvvisSpectrum', 'UvvisSpectrum'), ('IrPeak', 'IrPeak'), ('IrSpectrum', 'IrSpectrum'), ('NmrPeak', 'NmrPeak'), ('NmrSpectrum', 'NmrSpectrum'), ('GlassTransition', 'GlassTransition'), ('QuantumYield', 'QuantumYield'), ('FluorescenceLifetime', 'FluorescenceLifetime'), ('ElectrochemicalPotential', 'ElectrochemicalPotential'), ('NeelTemperature', 'NeelTemperature'), ('CurieTemperature', 'CurieTemperature'), ('InteratomicDistance', 'InteratomicDistance'), ('CoordinationNumber', 'CoordinationNumber'), ('CNLabel', 'CNLabel')))
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in allowed_ext:
            raise forms.ValidationError("Only these file formats are allowed: "
                                        + ", ".join(allowed_ext) + ".")
        # return cleaned data is very important.
        return file
