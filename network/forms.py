from .models import *
from django.forms import ModelForm




class AddFollowed(ModelForm):
    class Meta:
        model = Following
        fields = '__all__'

class AddComment(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'