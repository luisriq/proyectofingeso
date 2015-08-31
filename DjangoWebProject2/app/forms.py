# -*- coding: utf-8 -*-
"""
Definition of forms.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import ModelForm
from models import *
from datetime import datetime, timedelta, date


class UserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'correo', 'contrasena')
        
class CrearBandaForm(forms.Form):
    nombre = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control validate'}))
    choice_g = [ (gen.nombre,gen.nombre) for gen in Genero.objects.all()]
    choice_y = [(str(year), year) for year in range(1900, 2016) ]
    choice_y.reverse()
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septembrie", "Octubre", "Noviembre", "Diciembre"]
    choice_m = []
    for i in range(1,12):
        choice_m.append((i, meses[i]))
        
    
    genero = forms.ChoiceField(choices = choice_g, widget=forms.Select({
                                   'class': 'browser-default'}))
    mes = forms.ChoiceField(choices = choice_m, widget=forms.Select({
                                   'class': 'browser-default'}))
    year = forms.ChoiceField(choices = choice_y, widget=forms.Select({
                                   'class': 'browser-default'}))
    
class RegistroForm(forms.Form):
    name = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control validate'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'id':'contras',
                                   'class': 'form-control validate'}))
    password2 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'id':'contras2',
                                   'class': 'form-control validate'}))
    email = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'type':'email',
                                   'class': 'form-control validate'}))
    tipo = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("Debe confirmar su contraseña")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
class LoginForm(forms.Form):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'type':'email',
                                   'class': 'form-control validate'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'id':'contras',
                                   'class': 'form-control validate'}))
        
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'type':'email',
                                   'class': 'form-control validate'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'id':'contras',
                                   'class': 'form-control validate'}))
