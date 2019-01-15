from django import forms


class BuscarRestaurante(forms.Form):
    nombre = forms.CharField(label='Nombre Restaurante',max_length=100)



class BuscarPlato(forms.Form):
    nombre = forms.CharField(label = 'Nombre Plato',max_length=100)


class BorrarPlato(forms.Form):
    nombre_borrar = forms.CharField(label = 'Nombre Plato',max_length=100)