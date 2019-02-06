from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from game.models import Game, Category


def get_categories():
    categories = Category.objects.all()
    return tuple(map(lambda u: (str(u.id), u.name), categories))

class GameForm_old(forms.Form):
    game_name = forms.CharField(label='Name', max_length=100, required=True, help_text='100 characters max.',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    game_description = forms.CharField(label='Description', required=True,
                                       widget=forms.Textarea(attrs={'class': 'form-control text-text-text', }))
    game_url = forms.URLField(label='URL', required=True, initial='http://',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    game_image = forms.ImageField(label='Image', required=False)
    game_price = forms.FloatField(label='Price', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    game_category = forms.MultipleChoiceField(label='Category', required=True,
                                              help_text="Hold down [Control], or [Command] on a Mac, to select more than one.")
    game_category.widget.attrs.update({'class': 'form-control'})

    choice=((1,('True')),(2,('False')))
    game_available = forms.ChoiceField(choices=choice, label='Availability', required=False, initial='select', widget=forms.Select())
    game_available.widget.attrs.update({'class': 'form-control'})

    def __init__(self,*args,**kwargs):
        if 'game' in kwargs:
            game=kwargs.pop('game')
        else:
            game=None
        super(GameForm_old,self).__init__(*args,**kwargs)

        self.fields['game_category'].choices=get_categories()

        if(game):
            self.fields['game_name'].initial=game.name
            self.fields['game_description'].initial=game.description
            self.fields['game_url'].initial=game.url
            self.fields['game_image'].initial=game.image
            self.fields['game_price'].initial=game.price
            self.fields['game_available'].initial=game.available

    class Meta:
        model = Game



class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].initial='http://'
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].help_text = "Hold down [Control], or [Command] on a Mac, to select more than one."
        self.fields['category'].required = True
        self.fields['image'].label='Main Image'
        self.fields['image'].help_text ='Main image will show in home page and description page.'
        self.fields['image2'].label='Square Image'
        self.fields['image2'].help_text ='Square image will show in search page.'
        self.fields['release_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['release_date'].help_text = 'Format YYYY-MM-DD'
        self.fields['score_board'].help_text = 'Check, if the game will have score board'


    class Meta:
        model = Game
        fields = ['name','description', 'url','image','image2','price','available','release_date','score_board','category']

