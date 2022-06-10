from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, CartItem, Cart, CheckoutInfo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage

def home(request):
    product_list = Product.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    content = {'products':products}
    return render(request,'shop/home.html',content)

def product_detail(request, pk):
	product = Product.objects.filter(id=pk)
	return render(request, "shop/product_detail.html", {"prod":product[0]})

@login_required
def add_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    
    order_item,created = CartItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    
    order_qs = Cart.objects.filter(user = request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        
        #if item is already in the cart
        
        if order.item.filter(item__id = item.id).exists():
            order_item.quantity+=1
            order_item.save()
            CartItem.objects.filter(item = item,user = request.user, ordered=False).update(is_selected = True)
            
            messages.success(request, f'Your cart has been updated')
            return redirect('home')
        else:
            order.item.add(order_item)
            CartItem.objects.filter(item = item,user = request.user, ordered=False).update(is_selected = True)
            messages.success(request, f'This product is added to your cart')
            return redirect('home')
    else:
        order = Cart.objects.create(user = request.user)
        order.item.add(order_item)
        CartItem.objects.filter(item = item,user = request.user, ordered=False).update(is_selected = True)
        messages.success(request, f'This product is added to your cart')
        return redirect('home')


@login_required
def remove_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Cart.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #if item is already in the cart
        
        if order.item.filter(item__id = item.id).exists():
            order_item = CartItem.objects.filter(item = item,user = request.user, ordered=False)[0]
            
           
            CartItem.objects.filter(item = item,user = request.user, ordered=False).update(is_selected = False)
            CartItem.objects.filter(item = item,user = request.user, ordered=False).update(quantity = 1)
            order.item.remove(order_item)
            messages.warning(request, f'This product is removed from your cart')
    else:
        messages.info(request,"This item is not in your cart")
        return redirect('product-detail',pk=item.pk)
    return redirect('cart')



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user = request.user, ordered=False, is_selected=True)
    final_price = list(cart_items)
    
    total = 0
    for item in final_price:
        total += item.get_total_price()
    
    context = {
        'cart_items':cart_items,
        'total':total
        }
    
    
    return render(request,'shop/cart_view.html',context)

@login_required
def update_cart(request,pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id = pk)
        item = CartItem.objects.filter(user = request.user, ordered=False, is_selected=True, item = product).first()
        update_qty = request.POST['quantity']

        CartItem.objects.filter(user = request.user, ordered=False, is_selected=True, item = product).update(quantity=update_qty)
        messages.success(request, f'Cart updated!')
    return redirect('cart')
   

@login_required
def checkout_view(request):

    cart_items = CartItem.objects.filter(user = request.user, ordered=False, is_selected=True)
    
    final_price = list(cart_items)
    
    total = 0
    for item in final_price:
        total += item.get_total_price()
    
    


    if request.method=='POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            
            
            address=form.cleaned_data.get('address')
            apartment_address=form.cleaned_data.get('apartment_address')
            country=form.cleaned_data.get('country')
            pin=form.cleaned_data.get('pin')
            phone_number = form.cleaned_data.get('phone_number')

            checkout_info = CheckoutInfo(
                user = request.user,
                address = address,
                apartment_address = apartment_address,
                country = country,
                pin = pin,
                phone_number = phone_number

            )
            checkout_info.save()
            Cart.objects.filter(user = request.user, ordered=False).update(billing_address=checkout_info, ordered=True)
            CartItem.objects.filter(user = request.user,ordered=False,is_selected=True).update(ordered=True)
            messages.success(request, f'Successful Checkout! Check your inbox for confirmation mail')

            subject = 'FlyBuy: Thank You for your order'
            message = 'This email confirms your order'
            from_email = settings.EMAIL_HOST_USER
            print(from_email)
            to_list = [request.user.email]
            print(to_list)
            send_mail(subject,message,from_email,to_list,fail_silently = True)
            msg = EmailMessage(subject,
                       message, to_list)
            msg.send()
            return redirect('checkout')

    else:
        form =  CheckoutForm()

    context = {
        'cart_items':cart_items,
        'total':total,
        'form':form
        }
  
    return render(request,'shop/checkout.html',  context)




