from django.forms import ModelForm, Form, CharField
from .models import *
class CreateCollection(ModelForm):
    
    class Meta:
        model = Collection
        fields =['title','description']

class CreateDataSource(ModelForm):

    class Meta:
        model = DataSource
        fields = ['document_folder_name', 'collection', 'file']
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)

        super(CreateDataSource, self).__init__(*args, **kwargs)
        if current_user:
            self.fields['collection'].queryset = self.fields['collection'].queryset.filter(owner=current_user.id)

class QueryBot(Form):
    query = CharField(max_length=100)

class CreateGroupChatForm(ModelForm):

    class Meta:
        model = Room
        fields = ['members']
    # show only bots/collections created by the current user