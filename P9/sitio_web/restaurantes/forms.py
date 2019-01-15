from django import forms


class BuscarRestaurante(forms.Form):
    nombre = forms.CharField(label='Nombre Restaurante',max_length=100)



    