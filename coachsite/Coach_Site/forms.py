from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment,Coach, AvailableSlot


User = get_user_model()

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'coach', 'raiting']
        labels = {
            'text': 'Содержание',
            'raiting': 'Рейтинг',
            'coach': 'Тренер',
        }
        widgets = {

            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите текст поста'}),
            'raiting': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите рейтинг'}),
            'coach': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        text = self.cleaned_data['text']
        if len(text) < 5:
            raise forms.ValidationError("Заголовок не должен содержать не менее 5 символов")
        return text

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Рейтинг должен быть в диапазоне от 0 до 50")
        return rating

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('text')
        forbidden_words = ['казино', 'криптовалюта', 'крипта']
        if content:
            for word in forbidden_words:
                if word in content.lower():
                    raise forms.ValidationError(f"Содержание поста не должно содержать слово '{word}'")

        return cleaned_data


class CommentDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Подтвердите удаление",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'raiting']  # Исключаем coach и author
        labels = {
            'text': 'Содержание',
            'raiting': 'Рейтинг',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'raiting': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'age', 'height', 'weight']  # Поля для редактирования
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone_number': 'Номер телефона',
            'age': 'Возраст',
            'height': "Рост",
            'weight': "Вес"
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CoachEditForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['bio', 'experience_years', 'hide_phone_number']
        labels = {
            'bio': 'Биография',
            'experience_years': 'Стаж (лет)',
            'hide_phone_number': 'Скрыть номер телефона',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'hide_phone_number': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                               widget=forms.EmailInput(attrs={'class': 'form-control'})) # Добавляем email

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "age")


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))


class AvailableSlotForm(forms.ModelForm):
    class Meta:
        model = AvailableSlot
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }