from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Gasto, Cartao, Categoria

from django import forms
from .models import Gasto, Cartao, Categoria

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['cartao', 'valor', 'data', 'categoria', 'descricao', 'parcelas']
        widgets = {
            'cartao': forms.Select(attrs={'class': 'text-sm'}),
            'valor': forms.NumberInput(attrs={'class': 'text-sm'}),
            'data': forms.DateInput(attrs={'class': 'text-sm'}),
            'categoria': forms.Select(attrs={'class': 'text-sm'}),
            'descricao': forms.TextInput(attrs={'class': 'text-sm'}),
            'parcelas': forms.NumberInput(attrs={'class': 'text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        # Adicionando placeholder ao campo 'cartao'
        self.fields['cartao'].widget = forms.Select(
            choices=[('', 'Selecione um cartão')] + list(self.fields['cartao'].choices)[1:],
            attrs={'class': 'text-sm text-gray-100'}
        )
        # Adicionando placeholder ao campo 'categoria'
        self.fields['categoria'].widget = forms.Select(
            choices=[('', 'Escolha uma categoria')] + list(self.fields['categoria'].choices)[1:],
            attrs={'class': 'text-sm text-gray-200'}
        )


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'text-sm'}),
        }






class CartaoForm(forms.ModelForm):
    vencimento = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)],
                                    help_text="Informe um dia entre 1 e 31")

    class Meta:
        model = Cartao
        fields = ['nome', 'limite', 'vencimento', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control'}),
            'vencimento': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        
class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(label="Confirma a exclusão?", required=True)
    
    