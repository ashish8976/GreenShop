from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from . models import User, Category, Product, Wishlist
from django.conf import settings
from django.core.mail import send_mail
import random,time
from django.db.models import Avg

# Create your views here.

def register(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            msg = "User Already Exists"
            return render (request, 'register.html', {'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname = request.POST['fname'],
                    lname = request.POST['lname'],
                    email = request.POST['email'],
                    phone_number = request.POST['phone_number'],
                    password = make_password(request.POST['password'])
                )
                msg = "Registration Successfull !!"
                return render(request, 'login.html', {'msg':msg})
            else:
                msg = 'Password and Confirm Password is not match'
                return render(request, 'register.html',{'msg':msg})
    else:
        return render(request,'register.html')


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            if check_password(request.POST['password'],user.password):
                request.session['useremail'] = user.email
                request.session['username'] = user.fname 
                return redirect('index')
            else:
                msg = "password is not correct ? Plase Enter valid Password !!"
                return render(request, 'login.html',{'msg':msg})
        except User.DoesNotExist:
            msg = "Email Doesn't Exists"
            return render(request,'login.html', {'msg':msg})
    else:
        return render(request,'login.html')
         
def logout(request):
    request.session.flush()
    return redirect('login')


def update_password(request):
    if request.method == "POST":
        user = User.objects.get(email= request.session['useremail'])
        if check_password(request.POST['oldpassword'],user.password):
            if request.POST['newpassword']==request.POST['cpassword']:
                user.password = make_password(request.POST['newpassword'])
                user.save()
                msg = "Password Updated Successfully !!"
                return render(request,'login.html', {'msg':msg})
            else:
                msg = "New Password and Confirm Password is not match"
                return render(request, 'update_password.html', {'msg':msg})
        else:
            msg = "Old password is not correct!"
            return render(request,'update_password.html',{'msg':msg})
    else:
        return render(request,'update_password.html')


def forget_password(request):
    if request.method == "POST":
        step = request.POST.get('step') 
        if step == 'email':
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                otp = random.randint(100001,999999)
                subject = "OTP For Forget Password"
                message = f"Hy {user.fname} {user.lname} your otp  is {str(otp)}"
                email_from  = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail(
                         subject,
                             message,
                                email_from,
                                     recipient_list,
                                        fail_silently=False
                )
                request.session['useremail'] = user.email
                request.session['otp'] = str(otp)
                request.session['otp_time'] = time.time()
                return render(request,'forget_password.html',{
                            'show_otp' : True,
                                'email' : email,
                                     'msg' : 'Otp Send your Register Email'
                    })
            except User.DoesNotExist:
                 msg = "Email is not Exists"
                 return render(request,'forget_password.html',{'msg':msg})
        elif step == 'otp':
            entered_otp = request.POST.get('otp')
            session_otp = request.session.get('otp')
            otp_time = request.session.get('otp_time')
            email = request.session.get('useremail')

            if not session_otp or not otp_time:
                msg = "Session Expires Try Again"
                return render(request,'forget_password.html',{'msg':msg})
            
            if not otp_time or (time.time() - otp_time) > 600:
                msg = "OTP Expired. Please Try Again !!!"
                return render(request,'forget_password.html',{'msg':msg})
            
            if entered_otp == session_otp:
                del request.session['otp']
                del request.session['otp_time']
                return redirect('changepassword')
            else:
                msg = "OTP is not Correct Please Enter Valid OTP !!"
                return render(request,'forget_password.html',{
                    'show_otp':True,
                    'email':email,
                    'msg':msg
                })
        else:
            print("Not Found")
    else:
        return render(request,'forget_password.html')


def changepassword(request):
    if request.method == "POST":
        email = request.session.get('useremail')

        if not email:
            return redirect('forget_password')
        try:
            user = User.objects.get(email=email)
            newpassword = request.POST.get('newpassword')
            cpassword = request.POST.get('cpassword')

            if newpassword == cpassword:
                user.password = make_password(newpassword)
                user.save()
                del request.session['useremail']
                return redirect('login')
            else:
                msg = 'Password and Confirm Password is not Match, Plase Check your password !!'
                return render(request,'changepassword.html',{'msg':msg})
        except User.DoesNotExist:
            msg = "User not found"
            return render(request,'changepassword.html',{'msg',msg})
    else:
        return render(request,'changepassword.html')


def toggle_wishlist(request, product_id):
    if not request.session.get('useremail'):
        return redirect('login')
    user = User.objects.get(email=request.session['useremail'])
    product = Product.objects.get(id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=user, product=product)
    if not created:
        obj.delete()
    return redirect(request.META.get('HTTP_REFERER', 'products'))

def wishlist(request):
    if not request.session.get('useremail'):
        return redirect('login')
    user = User.objects.get(email=request.session['useremail'])
    items = Wishlist.objects.filter(user=user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': items})


def category(request):
    category = Category.objects.all()
    return render(request, 'category.html', {'category': category})

def category_products(request, cat_id):
    try:
        selected_category = Category.objects.get(id=cat_id, is_active=True)
        products = Product.objects.filter(category=selected_category, is_active=True)
    except Category.DoesNotExist:
        selected_category = None
        products = []
    
    return render(request, 'category_products.html', {
        'selected_category': selected_category,
        'products': products,
    })

def account(request):
    user = User.objects.get(email= request.session['useremail'])
    msg = ""

    # DASHBOARD
  
    # MANAGE ORDERS

    # WISHLIST

    # ADDRESS

    # PROFILE IMAGE UPDATE
    if request.method == "POST" and request.FILES.get('user_image'):
        user.user_image = request.FILES.get('user_image')
        user.save()

        return redirect('account')

    # PROFILE UPDATE
    if request.method == "POST" and 'update_profile' in request.POST:
        try:

            user.fname = request.POST.get('fname')
            user.lname = request.POST.get('lname')
            user.phone_number = request.POST.get('phone_number')
            user.bio = request.POST.get('bio')

            user.save()

            message = "Profile Updated Successfully"
            return render(request, 'account.html', {
                    'message':message,
                    'user' : user,
                    'active_panel' : 'profile',
                })
        except:
            message = "Something Problem"
            return render(request, 'account.html', {
                    'message':message,
                    'user' : user,
                    'active_panel' : 'profile',
                })
        

    # CHANGE PASSWORD
    if request.method == "POST" and 'update_password' in request.POST:
        if check_password(request.POST['oldpassword'],user.password):
            if request.POST['newpassword']==request.POST['cpassword']:
                user.password = make_password(request.POST['newpassword'])
                user.save()
                msg = "Password Updated Successfully !!"
                return render(request,'login.html', {'msg':msg})
            else:
                msg = "New Password and Confirm Password is not match"
                return render(request, 'account.html', {
                    'msg':msg,
                    'user' : user,
                    'active_panel' : 'password',
                })
        else:
            msg = "Current password is not match"
            return render(request,'account.html',{ 
                'msg': msg,
                'user' : user,
                'active_panel' : 'password',
            })
        
        
    context = {
        'user': user,
        'msg': msg,
    }

    return render(request, 'account.html', context)



def index(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)[:8]
    return render(request, 'index.html', {
        'categories': categories,
        'products'  : products,
    })


def products(request):
    all_products = Product.objects.filter(is_active=True)
    categories   = Category.objects.filter(is_active=True)
    total_count  = all_products.count()

    # ── Category Filter ──────────────────────────
    selected_category = request.GET.get('category')
    if selected_category:
        all_products = all_products.filter(category__id=selected_category)

    # ── Price Filter ─────────────────────────────
    max_price = request.GET.get('max_price')
    if max_price:
        all_products = all_products.filter(sizes__variants__price__lte=max_price)

    # ── Search Filter ─────────────────────────────
    search = request.GET.get('search')
    if search:
        all_products = all_products.filter(name__icontains=search)

    # ── Sunlight Filter ───────────────────────────
    selected_sunlight = request.GET.get('sunlight')
    if selected_sunlight:
        all_products = all_products.filter(sunlight__icontains=selected_sunlight)

    # ── Air Purifying Filter ──────────────────────
    air_purifying = request.GET.get('air_purifying')
    if air_purifying:
        all_products = all_products.filter(air_purifying=True)

    # ── Sorting ───────────────────────────────────
    sort = request.GET.get('sort')
    if sort == 'price_low':
        all_products = all_products.order_by('sizes__variants__price')
    elif sort == 'price_high':
        all_products = all_products.order_by('-sizes__variants__price')
    elif sort == 'newest':
        all_products = all_products.order_by('-created_at')

    all_products = all_products.distinct()

    return render(request, 'products.html', {
        'products'         : all_products,
        'categories'       : categories,
        'total_count'      : total_count,
        'selected_category': selected_category,
        'max_price'        : max_price,
        'search'           : search,
        'selected_sunlight': selected_sunlight,
        'air_purifying'    : air_purifying,
        'sort'             : sort,
    })



def product_details(request, product_id):
    product = Product.objects.get(id=product_id, is_active=True)
    sizes   = product.sizes.all().prefetch_related('images', 'variants__pot')
    pots    = product.pots.all()
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    sizes_with_stock = {}
    for size in sizes:
        sizes_with_stock[size.id] = any(v.stock > 0 for v in size.variants.all())

    pots_with_stock = {}
    for pot in pots:
        pots_with_stock[pot.id] = any(v.stock > 0 for v in pot.variants.all())
    return render(request, 'product_detail.html', {
        'product': product,
        'sizes'  : sizes,
        'pots'   : pots,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'sizes_with_stock':sizes_with_stock,
        "pots_with_stock" : pots_with_stock,
    })


def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'checkout.html')

def wishlist(request):
    return render(request,'wishlist.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def track_order(request):
    return render(request,'track_order.html')

def order_tracking(request):
    return render(request,'order_tracking.html')




