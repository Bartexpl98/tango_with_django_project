from django import forms
from rango.models import Page,Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category._meta.get_field('name').max_length,min_length=1,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug  = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

    def clean_name(self):
        # Custom validation to check if a category with the same name already exists
        name = self.cleaned_data['name']
        existing_category = Category.objects.filter(name__iexact=name)

        if existing_category.exists():
            raise forms.ValidationError("Category with this Name already exists.")

        return name


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page._meta.get_field('title').max_length,
                            help_text="Please enter the title of the page.")
    url   = forms.URLField(max_length=Page._meta.get_field('url').max_length,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model=Page

        exclude = ("category", )

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
# If url is not empty and doesn't start with 'http://',
# then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data