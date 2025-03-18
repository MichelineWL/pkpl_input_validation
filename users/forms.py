from django import forms # type: ignore
import re
from django.core.exceptions import ValidationError # type: ignore
from datetime import date, timedelta

# Custom Validator untuk Username
def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9._-]+$', value):
        raise ValidationError("Username hanya boleh berisi huruf, angka, '.', '_', dan '-'.")
    return value

# Custom Validator untuk Tanggal Lahir (Minimal 12 tahun)
def validate_birthdate(value):
    min_age_date = date.today() - timedelta(days=12*365)
    if value > min_age_date:
        raise ValidationError("Usia minimal harus 12 tahun.")

# Custom Validator untuk Nomor HP
def validate_phone(value):
    if not re.match(r'^62[0-9]{6,13}$', value):  # 62- dihilangkan, hanya angka setelah 62
        raise ValidationError("Nomor HP harus dalam format 62XXXX dengan panjang 8-15 digit.")

# Form Django
class UserForm(forms.Form):
    nama = forms.CharField(
        max_length=255, 
        validators=[validate_username], 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    tanggal_lahir = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        validators=[validate_birthdate]
    )
    nomor_hp = forms.CharField(
        max_length=15,
        validators=[validate_phone],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    url_blog = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    deskripsi_diri = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        min_length=5,
        max_length=1000
    )

    # Status Perkawinan (Predefined Value)
    STATUS_PERKAWINAN_CHOICES = [
        ('Belum Kawin', 'Belum Kawin'),
        ('Kawin', 'Kawin'),
        ('Duda', 'Duda'),
        ('Janda', 'Janda'),
    ]
    status_perkawinan = forms.ChoiceField(
        choices=STATUS_PERKAWINAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # NPWP (Format XX.XXX.XXX.X-XXX.XXX)
    def validate_npwp(value):
        import re
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}\.\d{1}-\d{3}\.\d{3}$', value):
            raise ValidationError("Format NPWP harus XX.XXX.XXX.X-XXX.XXX, contoh: 12.345.678.9-012.345")
        return value

    npwp = forms.CharField(
        max_length=20,
        validators=[validate_npwp],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678.9-012.345'})
    )