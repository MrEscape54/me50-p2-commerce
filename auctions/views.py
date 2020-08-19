from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from .models import User, Category, Auction, Watchlist
from .forms import CommentForm, AuctionForm, BidForm


def index(request, category_slug=None):
    # if no category is provided get active listings
    auctions = Auction.active.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        # if category is provided get active listings by category
        auctions = Auction.active.filter(category=category)
    context = {'auctions': auctions, 'category': category}
    return render(request, "auctions/index.html", context)


def detail(request, auction):
    auction = get_object_or_404(Auction, slug=auction)
    comments = auction.comments.all()
    watchlisted = None
    comment_message = None
    bid_message = None
    new_comment = None
    new_bid = None

    if request.user.is_authenticated:
        watchlisted = any(item in auction.watchlist.all() for item in request.user.watchlist.all())
        
    if request.method == 'POST':
        # Instantiate both comment and bid form
        comment_form = CommentForm(data=request.POST)
        bid_form = BidForm(data=request.POST)
        # if submit is triggered in the comment form
        if request.POST.get("form_type") == 'form_comment':
            bid_form = BidForm()
            if not request.user.is_authenticated:
                comment_message = "You have to sign in to post a comment"
            else:
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.auction = auction
                    new_comment.user = request.user
                    new_comment.save()
                    return redirect('detail', auction.slug)
        # if submit is triggered in the bid form
        elif request.POST.get("form_type") == 'form_bid':
            comment_form = CommentForm()    
            if not request.user.is_authenticated:
                bid_message = "You have to sign in to place a bid"
            # Validate if new bid is greater than previous one.
            elif auction.bid.last() and (float(request.POST['bid']) <= auction.bid.last().bid):
                bid_message = "Your bid must be greater than the current price."
            # Validate if new bid is greater or equal than base price.
            elif not auction.bid.last() and (float(request.POST['bid']) < auction.base_price):
                bid_message = "Your bid can not be less than the current price."
            else:
                if bid_form.is_valid():
                    new_bid = bid_form.save(commit=False)
                    new_bid.auction = auction
                    new_bid.user = request.user
                    new_bid.save()
                    return redirect('detail', auction.slug)
    else: 
        comment_form = CommentForm()
        bid_form = BidForm()

    context = {'auction': auction, 
               'comments': comments, 
               'comment_form': comment_form, 
               'bid_form': bid_form,
               'new_comment': new_comment, 
               'new_bid': new_bid,
               'comment_message': comment_message,
               'bid_message': bid_message,
               'watchlisted': watchlisted
               }
               
    return render(request, 'auctions/detail.html', context)

@login_required
def watchlist(request):
    watchlisted = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlisted':watchlisted})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})

@login_required
def add_to_watchlist(request):
    auction = get_object_or_404(Auction, pk=request.GET.get('auction_id'))
    Watchlist.objects.get_or_create(user=request.user, auction=auction)  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_watchlist(request):
    auction = get_object_or_404(Auction, pk=request.GET.get('auction_id'))
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.get(user=request.user, auction=auction)
        watchlist.delete()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def close_auction(request):
    auction = get_object_or_404(Auction, pk=request.GET.get('auction_id'))
    if request.user.is_authenticated:
        auction.is_active = False
        auction.save()
        
    return redirect('index')

@login_required
def add_auction(request):
    if request.method == 'POST':
        form = AuctionForm(data=request.POST)
        if form.is_valid():
            print(form)
            auction = form.save(commit=False)
            auction.user = request.user
            auction.slug = slugify(auction.title)
            auction.save()
            return redirect('index')
    else:
        form = AuctionForm()
    return render(request, 'auctions/add_auction.html', {"form": form})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
