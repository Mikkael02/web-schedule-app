from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Adres e-mail"),
        help_text=_("Wprowadź prawidłowy adres e-mail.")
    )

    error_messages = {
        **UserCreationForm.error_messages,
        'password_mismatch': _("Hasła muszą być identyczne."),
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _("Nazwa użytkownika"),
        }
        help_texts = {
            'username': _("Wymagane. Maksymalnie 150 znaków. Dozwolone litery, cyfry oraz @/./+/-/_ ."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Zmiana etykiet i komunikatów pomocniczych dla pól
        self.fields['password1'].label = _("Hasło")
        self.fields['password1'].help_text = _(
            "Twoje hasło musi zawierać co najmniej 8 znaków, nie może być zbyt podobne "
            "do innych danych osobowych, nie może być często używanym hasłem i nie może składać się wyłącznie z cyfr."
        )
        self.fields['password2'].label = _("Potwierdzenie hasła")
        self.fields['password2'].help_text = _("Wprowadź to samo hasło ponownie w celu weryfikacji.")

        # Dodanie klasy CSS do wszystkich pól
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        """
        Sprawdza, czy oba pola haseł są zgodne.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Nazwa użytkownika"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź nazwę użytkownika")
        })
    )
    password = forms.CharField(
        label=_("Hasło"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź hasło")
        })
    )

    error_messages = {
        'invalid_login': _(
            "Proszę wprowadzić poprawną nazwę użytkownika i hasło. "
            "Uwaga: wielkość liter ma znaczenie."
        ),
        'inactive': _("To konto jest nieaktywne."),
    }

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Imię"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź swoje imię")
        })
    )
    last_name = forms.CharField(
        label=_("Nazwisko"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź swoje nazwisko")
        })
    )
    email = forms.EmailField(
        label=_("Adres e-mail"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź swój adres e-mail")
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        error_messages = {
            'username': {
                'required': _("To pole jest wymagane."),
                'max_length': _("Maksymalna długość to 150 znaków."),
            },
            'email': {
                'required': _("To pole jest wymagane."),
                'invalid': _("Podaj prawidłowy adres e-mail."),
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _("Wprowadź nazwę użytkownika")
        })
        self.fields['username'].label = _("Nazwa użytkownika")
        self.fields['username'].help_text = _("Maksymalnie 150 znaków. Dozwolone litery, cyfry oraz @/./+/-/_.")

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Stare hasło"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź swoje stare hasło")
        }),
        error_messages={
            'required': _("To pole jest wymagane."),
            'invalid': _("Podano nieprawidłowe stare hasło."),
        }
    )
    new_password1 = forms.CharField(
        label=_("Nowe hasło"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź swoje nowe hasło")
        }),
        help_text=_("Hasło musi mieć co najmniej 8 znaków, zawierać litery i cyfry oraz nie być zbyt proste."),
    )
    new_password2 = forms.CharField(
        label=_("Potwierdź nowe hasło"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Wprowadź nowe hasło ponownie")
        }),
        error_messages={
            'required': _("To pole jest wymagane."),
            'invalid': _("Hasła nie pasują."),
        }
    )