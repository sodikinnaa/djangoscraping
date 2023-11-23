# forms.py

from django import forms
from .models import Universitas


class add_universitas(forms.ModelForm):
    class Meta:
        model = Universitas
        fields = ["nama_univ", "url_univ", "total_sitasi"]

    def clean_url_univ(self):
        url_univ = self.cleaned_data.get("url_univ")
        if Universitas.objects.filter(url_univ=url_univ).exists():
            raise forms.ValidationError(
                "URL universitas sudah ada. Gunakan URL yang berbeda."
            )
        return url_univ
