from django import forms
from . import models
from . import config


class ProductsForm(forms.ModelForm):
    # p_cat = forms.ChoiceField(widget=forms.Select())
    p_cat = forms.ModelChoiceField(queryset=models.Category_products.objects.all())
    name = forms.CharField(max_length=config.CHARS_DEFAULT, required=True)
    description = forms.CharField(max_length=200)
    quantity = forms.IntegerField(max_value=99, min_value=1, step_size=1)
    price = forms.DecimalField(max_value=99999, min_value=1, step_size=0.1, required=True)
    cur_img = forms.ImageField(
        label='Product current img',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': False})
    )

    class Meta:
        model = models.Products
        fields = ('p_cat', 'name', 'description', 'quantity', 'price', 'cur_img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = models.Category_products.objects.all()
        choices = [(category.id, str(category)) for category in categories]
        self.fields['p_cat'].choices = choices
