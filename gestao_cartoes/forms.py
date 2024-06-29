from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Gasto, Cartao, Categoria

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['cartao', 'valor', 'data', 'categoria', 'descricao', 'parcelas']
        widgets = {
            'cartao': forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight'}),
            'data': forms.DateInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
        }

class CartaoForm(forms.ModelForm):
    vencimento = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)],
                                    help_text="Informe um dia entre 1 e 31")

    class Meta:
        model = Cartao
        fields = ['nome', 'limite', 'vencimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            # Adicione widgets para os outros campos conforme necessário
        }