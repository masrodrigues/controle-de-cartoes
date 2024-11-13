from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Gasto, Cartao, Categoria

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['cartao', 'valor', 'data', 'categoria', 'descricao', 'parcelas']
        widgets = {
            'cartao': forms.Select(attrs={'class': 'text-sm'}),
            'valor': forms.NumberInput(attrs={'class': 'text-sm'}),
            'data': forms.DateInput(attrs={'class': 'text-sm', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'text-sm'}),
            'descricao': forms.TextInput(attrs={'class': 'text-sm', 'placeholder': 'Descrição do gasto'}),
            'parcelas': forms.NumberInput(attrs={'class': 'text-sm', 'min': 1, 'max': 36, 'placeholder': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cartao'].widget.attrs.update({
            'placeholder': 'Selecione um cartão',
            'class': 'text-sm'
        })
        self.fields['categoria'].widget.attrs.update({
            'placeholder': 'Escolha uma categoria',
            'class': 'text-sm'
        })

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'text-sm',
                'placeholder': 'Nome da Categoria'
            }),
        }

class CartaoForm(forms.ModelForm):
    vencimento = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text="Informe um dia entre 1 e 31"
    )

    class Meta:
        model = Cartao
        fields = ['nome', 'limite', 'vencimento', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Cartão'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Limite do Cartão'}),
            'vencimento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dia do Vencimento'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(label="Confirma a exclusão?", required=True)
