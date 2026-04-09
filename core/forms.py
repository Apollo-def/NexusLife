from django import forms # Importa o módulo de formulários do Django.
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django.
from django.contrib.auth.forms import UserCreationForm # Formulário base do Django para criação de usuários.
from .models import UserProfile


# Formulário de registro de usuário, herdando e estendendo o UserCreationForm.
class UserRegisterForm(UserCreationForm):
    PERSON_TYPE_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]

    person_type = forms.ChoiceField(
        choices=PERSON_TYPE_CHOICES,
        initial='PF',
        widget=forms.RadioSelect()
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    cpf_cnpj = forms.CharField(
        max_length=18,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF ou CNPJ'}),
        label='CPF / CNPJ'
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DDD) Telefone'})
    )
    state_registration = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual (para PJ)'}),
        label='Inscrição Estadual'
    )
    cep = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000', 'id': 'id_cep'}),
        label='CEP'
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço', 'readonly': 'readonly'}),
        label='Endereço'
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade', 'readonly': 'readonly'}),
        label='Cidade'
    )
    state = forms.CharField(
        max_length=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UF', 'readonly': 'readonly'}),
        label='Estado'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].required = False
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Senha'
        self.fields['person_type'].widget.attrs['class'] = 'form-check-input'

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data.get('person_type')
        cpf_cnpj = cleaned_data.get('cpf_cnpj', '')

        if person_type == 'PF' and cpf_cnpj:
            if not self.validate_cpf(cpf_cnpj):
                self.add_error('cpf_cnpj', 'CPF inválido.')
        elif person_type == 'PJ' and cpf_cnpj:
            if not self.validate_cnpj(cpf_cnpj):
                self.add_error('cpf_cnpj', 'CNPJ inválido.')

        return cleaned_data

    @staticmethod
    def validate_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        # Validação dos dígitos verificadores (simplificada)
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = (sum1 * 10 % 11) % 10
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = (sum2 * 10 % 11) % 10
        return int(cpf[9]) == digit1 and int(cpf[10]) == digit2

    @staticmethod
    def validate_cnpj(cnpj):
        cnpj = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        # Validação dos dígitos verificadores
        weights1 = [5,4,3,2,9,8,7,6,5,4,3,2]
        sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 0 if sum1 % 11 < 2 else 11 - (sum1 % 11)
        weights2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
        sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 0 if sum2 % 11 < 2 else 11 - (sum2 % 11)
        return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2


class LoginForm(forms.Form):
    # Campo para o usuário inserir seu nome de usuário (ou email/CPF, dependendo da lógica de autenticação).
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email ou seu CPF'}))
    # Campo para a senha.
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))


class UserUpdateForm(forms.ModelForm):
    """
    Formulário para atualizar os dados do usuário (nome, sobrenome, email).
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
