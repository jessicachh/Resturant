from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
from.models import Category,Momo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Momo, CartItem, Order, OrderItem


from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.
def index(request):
    category = Category.objects.all()
    cateid = request.GET.get('category')  # Get selected category

    if cateid:
        momo = Momo.objects.filter(category=cateid)
        selected_category = int(cateid)  # Pass to template
    else:
        momo = Momo.objects.all()
        selected_category = None  # No category selected
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']

        Contact.objects.create(name=name,email=email,phone=phone,message=message)
        try:
            subject = "Thanks for Contacting BITE"
            message_body = f"Hi {name},\n\nThank you for contacting us. We have received your message:\n\n{message_text}\n\n- BITE Team"
            from_email = 'jsscraut@gmail.com'  # must match EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

        except Exception as e:
            print("Error sending email:", e)  # Check console if email fails
            messages.error(request, "There was an error sending the confirmation email.")

        messages.success(request, "Your form was successfully submitted! Please check your email.")
        return redirect('index')

    context = {
        'date': datetime.now(),
        'category': category,
        'momo': momo,
        'selected_category': selected_category
    }
    return render(request, 'core/index.html', context)

# @login_required(login_url='login')
def about(request):
    return render(request,'core/about.html')

def contact(request):
    return render(request,'core/contact.html')


def menu(request):
    category = Category.objects.all()             # get all categories
    cateid = request.GET.get('category')          # get selected category from URL

    if cateid:
        momo = Momo.objects.filter(category=cateid)  # filter momos by category
        selected_category = int(cateid)
    else:
        momo = Momo.objects.all()                    # show all momos if no category
        selected_category = None

    context = {
        'category': category,
        'momo': momo,
        'selected_category': selected_category,
    }
    return render(request, 'core/menu.html', context)


def services(request):
    return render(request,'core/services.html')

def cart(request):
    return render(request,'core/cart.html')

def index(request):
    category = Category.objects.all()
    cateid = request.GET.get('category')

    if cateid:
        momo = Momo.objects.filter(category=cateid)
        current_category = int(cateid)  # use the same name as template
    else:
        momo = Momo.objects.all()
        current_category = None

    context = {
        'date': datetime.now(),
        'category': category,
        'momo': momo,
        'current_category': current_category,  # 🔑 match template
    }
    return render(request, 'core/index.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Momo, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Add success message
    messages.success(request, f"✅ {product.name} added to your cart!")

    # Redirect back to the same item (using anchor)
    next_url = request.POST.get('next', 'menu')
    return redirect(next_url)

@login_required(login_url='login')
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')

@login_required(login_url='login')
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.total_price() for item in cart_items)
    shipping = 50 if subtotal > 0 else 0  # flat shipping fee
    total = subtotal + shipping
    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })
    
    # Checkout modal
@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # Prevent placing order if cart is empty
    if not cart_items.exists():
        messages.error(request, "❌ Your cart is empty. Please add items before placing an order.")
        return redirect("cart")

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        # Calculate total order amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total=total_amount,
        )

        # Save each cart item as order item and prepare for email
        order_items = []
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Add total attribute for email template
            order_item.total = item.quantity * item.product.price
            order_items.append(order_item)

        # Clear cart
        cart_items.delete()

        # Prepare admin emails
        admin_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
        admin_emails += ["aayushbasnet745@gmail.com", "selikaryee@gmail.com"]  # Extra admin emails

        # Send HTML email to admins
        if admin_emails:
            subject = f"New Order #{order.id} Placed!"
            html_content = render_to_string("core/admin_order_email.html", {
                "order": order,
                "order_items": order_items,
            })
            email = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, admin_emails)
            email.content_subtype = "html"
            email.send(fail_silently=False)

        # Success message for customer
        messages.success(request, f"✅ Your order has been placed successfully!")
        return redirect("cart")

    return redirect("cart")
