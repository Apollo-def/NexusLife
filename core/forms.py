from django import forms # Importa o módulo de formulários do Django.
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django.
from django.contrib.auth.forms import UserCreationForm # Formulário base do Django para criação de usuários.


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
    cpf = forms.CharField(
        max_length=18,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DDD) Telefone'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Senha'


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
