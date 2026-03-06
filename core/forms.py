from django import forms # Importa o módulo de formulários do Django.
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django.
from django.contrib.auth.forms import UserCreationForm # Formulário base do Django para criação de usuários.


# Formulário de registro de usuário, herdando e estendendo o UserCreationForm.
class UserRegisterForm(UserCreationForm):
    # Adiciona um campo de email, que é obrigatório.
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    # Adiciona um campo para o primeiro nome (opcional).
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    # Adiciona um campo para o sobrenome (opcional).
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    # Adiciona um campo para o CPF (opcional).
    cpf = forms.CharField(
        max_length=14, # Ex: 123.456.789-10
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'})
    )
    class Meta:
        model = User # Especifica que este formulário está associado ao modelo User.
        # Lista os campos do modelo que devem ser incluídos no formulário.
        fields = ('username', 'first_name', 'last_name', 'email', 'cpf', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        # O método __init__ é usado para customizar os campos do formulário.
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control' # Adiciona classe CSS ao campo username.
        self.fields['password1'].widget.attrs['class'] = 'form-control' # Adiciona classe CSS ao campo de senha.
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha' # Adiciona placeholder.
        self.fields['password2'].widget.attrs['class'] = 'form-control' # Adiciona classe CSS ao campo de confirmação de senha.
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Senha' # Adiciona placeholder.


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
