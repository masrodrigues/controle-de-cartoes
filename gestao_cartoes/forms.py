from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Gasto, Cartao, Categoria

from django import forms
from .models import Gasto, Cartao, Categoria

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['cartao', 'valor', 'data', 'categoria', 'descricao', 'parcelas']

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        # Adicionando placeholder ao campo 'cartao'
        self.fields['cartao'].widget = forms.Select(
            choices=[('', 'Selecione um cartão')] + list(self.fields['cartao'].choices)[1:],
            attrs={'class': 'sua-classe-css'}
        )
        # Adicionando placeholder ao campo 'categoria'
        self.fields['categoria'].widget = forms.Select(
            choices=[('', 'Escolha uma categoria')] + list(self.fields['categoria'].choices)[1:],
            attrs={'class': 'sua-classe-css'}
        )

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