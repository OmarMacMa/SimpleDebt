from django import forms


class RegisterForm(forms.Form):
    group_name = forms.CharField(max_length=50, required=True, label="Group name", widget=forms.TextInput(attrs={"class": "form-text"}))
    user_paying = forms.CharField(max_length=50, required=True, label="Who paid", widget=forms.TextInput(attrs={"class": "form-text"}))
    users_receiving = forms.CharField(max_length=200, required=True, label="Who received (separate with commas, no spaces, e.g. 'John,Paul,George,Ringo')", widget=forms.TextInput(attrs={"class": "form-text"}))
    amount = forms.DecimalField(decimal_places=2, max_digits=10, required=True, label="Amount (e.g. 12.34)", widget=forms.NumberInput(attrs={"class": "form-number"}))
    date = forms.DateField(input_formats=['%d/%m/%Y', '%d/%m/%y'], required=True, label="Date (dd/mm/yyyy)", widget=forms.DateInput(attrs={"class": "form-date"}))
    description = forms.CharField(max_length=50, required=True, label="Description (e.g. 'McDonalds, Cinema, etc.')", widget=forms.TextInput(attrs={"class": "form-text"}))
