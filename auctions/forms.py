from django import forms
from auctions.models import Comment, Auction, Bid

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Write your message here'}),
            'auction' : forms.HiddenInput(),
            'user' : forms.HiddenInput(),
        }

class AuctionForm(forms.ModelForm):
    
    class Meta:
        model = Auction
        fields = ("title", "description", "base_price", "image", "category")

        widgets = {
            'user': forms.HiddenInput(),
        }


class BidForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bid'].widget.attrs.update({'placeholder': 'Your bid', 'step': 1})
    
    class Meta:
        model = Bid
        fields = ('bid',)
    
        widget = {
            'user': forms.HiddenInput(),
            'auction': forms.HiddenInput()
        }



