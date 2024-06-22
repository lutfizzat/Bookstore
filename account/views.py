from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AddressForm
from django.db.models import Q
from .models import *
from account.extras import generate_order_id
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse


class HomePageView(ListView):
    model = Item
    template_name = 'account/homepage.html'

@method_decorator(login_required, name='dispatch')
class BookDetail(DetailView):
    model = Item
    template_name = 'account/bookprofile.html'

@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'order':order
        }
        return render(self.request, 'account/cart_summary.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = AddressForm()
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'form':form,
            'order':order
        }
        return render(self.request, 'account/checkout.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        form = AddressForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            save_info = form.cleaned_data.get('save_info')
            use_default = form.cleaned_data.get('use_default')
            payment_choice = form.cleaned_data.get('payment_choice')

            address = Address(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
            )
            address.save()
            # check if tick set as default address
            if save_info:
                address.default = True
                address.save()
            order.address = address
            order.save()
            print(form.cleaned_data)
            return redirect('checkout')
        else:
            print('form invalid')
            return redirect('checkout')

@login_required(login_url='login')
def search_venue_view(request):
    srh = request.GET['query']
    items = Item.objects.filter(title__icontains=srh)
    params = {'items':items,'search':srh}
    return render(request, 'account/search_venue.html', params)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #form.save()
            #email = form.cleaned_data.get('email')
            #raw_password = form.cleaned_data.get('password1')
            account = form.save()
            account.type = form.cleaned_data['usertype']
            account.save()
            login(request, account)
            return redirect('homepage')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

@login_required(login_url='login')  
def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):

    context ={}

    user = request.user
    if user.is_authenticated:
        return redirect("homepage")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return redirect("home")
            #     else:
            #         return AccountAuthenticationForm("invalid")


            if user:
                login(request, user)
                return redirect("homepage")
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)

@login_required(login_url='login')
def profile_view(request):
    context = {}
    return render(request, 'account/profile.html', context)


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # unique issue
    order_item, created = OrderItem.objects.get_or_create(item=item)
    order_qs = Order.objects.filter(user=request.user, is_ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item.title}'s quantity was updated")
            return redirect('cart_summary')
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item.title} was added to your cart")
            return redirect('cart_summary')
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(user=request.user, is_ordered=False, date_ordered=date_ordered)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item.title} was added to your cart")
        return redirect('cart_summary')


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item)
    order_qs = Order.objects.filter(user=request.user, is_ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.title} was removed from cart")
            return redirect('cart_summary')
        else:
            messages.info(request, f"{item.title} was not in your cart")
            return redirect('cart_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('cart_summary')


def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item)
    order_qs = Order.objects.filter(user=request.user, is_ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item.title} was removed from cart")
            return redirect('cart_summary')
        else:
            messages.info(request, f"{item.title} was not in your cart")
            return redirect('cart_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('cart_summary')

@login_required(login_url='login')
def book_collection_view(request):
    item = Item.objects.all()
    context = {'item':item}
    return render(request, 'account/book_collection.html', context)        

@login_required(login_url='login')
def account_delete_view(request):  
    if request.user.is_authenticated:
        context = {}
        user = request.user
        user.delete()
        return render(request, 'account/account_delete.html', context)
    else:
        return HttpResponse(request,"you haven't logged in into any accounts")

@login_required(login_url='login')
def payment_complete_view(request):   
    return render(request, 'account/payment_complete.html')

@login_required(login_url='login')
def successpurchase_view(request):   
    return render(request, 'account/successpurchase.html')

   

