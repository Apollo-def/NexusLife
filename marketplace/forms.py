from django import forms
from .models import Category, Service, Order, FreelancerProfile

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category', 'delivery_days', 'revisions']
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'price': 'Preço (R$)',
            'category': 'Categoria',
            'delivery_days': 'Prazo de Entrega (dias)',
            'revisions': 'Número de Revisões',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Desenvolvimento de Website em Django'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva seu serviço em detalhes...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '100.00'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'delivery_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'revisions': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adicione notas ou instruções especiais...'}),
        }

class FreelancerProfileForm(forms.ModelForm):
    """Form for PF/PJ freelancer profile"""
    class Meta:
        model = FreelancerProfile
        fields = ['person_type', 'business_name', 'cnpj', 'state_registration', 'bio', 'profile_image', 'hourly_rate', 'location', 'phone', 'website', 'response_time']
        widgets = {
            'person_type': forms.Select(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'state_registration': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'response_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
