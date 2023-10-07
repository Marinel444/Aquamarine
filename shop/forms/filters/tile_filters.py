from django import forms


class TileFilterForm(forms.Form):
    SIZE_CHOICES = [
        ('', 'Выберите размер'),
        ('60x60', '60x60'),
        ('120x60', '120x60'),
        ('43x43', '43x43'),
    ]
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False, label='Размер')
