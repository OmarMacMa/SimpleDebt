from django import forms


class RegisterForm(forms.Form):
    group_name = forms.CharField(max_length=50, required=True, label="Group name")
    user_paying = forms.CharField(max_length=50, required=True, label="Who paid")
    users_receiving = forms.CharField(max_length=200, required=True, label="Who received (separate with commas, no spaces, e.g. 'John,Paul,George,Ringo')")
    amount = forms.DecimalField(decimal_places=2, max_digits=10, required=True, label="Amount (e.g. 12.34)")
    date = forms.DateField(input_formats=['%d/%m/%Y', '%d/%m/%y'], required=True, label="Date (dd/mm/yyyy)")
    description = forms.CharField(max_length=50, required=True, label="Description (e.g. 'McDonalds, Cinema, etc.')")
