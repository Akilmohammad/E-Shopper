from django.shortcuts import render, redirect
from . models import User, CONTACT, WOMEN_CLOTH, MEN_CLOTH, Transaction, WOMEN_ACCESSORIES, MEN_ACCESSORIES, WOMEN_FOOTWEAR, MEN_FOOTWEAR, WISHLIST, CART, CHECKOUT
from django.core.mail import send_mail
import random
from django.conf import settings
import json
from django.http import request, request, request, request, request
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from PyPDF2 import pdf
import html
# import requests

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

# checkout = CHECKOUT.objects.get(all)

data = {
	"company": "Dennnis Ivanov Company",
	"address": "address",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response

# Create your views here.


def initiate_payment(request):
    try:
        # checkout = CHECKOUT.objects.get(fname=)
        amount = int(request.POST['net'])
        fname = request.POST['fname']
        print("First Name : ",fname)
        lname = request.POST['lname']
        print("Last Name : ",lname)
        # print('akil')
        user = User.objects.get(email=request.session['email'])
    except:
        return render(request, 'mycart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount,fname=fname,lname=lname)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        #('FIRSTNAME',str(transaction.fname)),
        # ('LASTNAME',transaction.lname),
        # ('ADDRESS',CHECKOUT.add1),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        print("Received Data : ",received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(
            paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)


def index(request):
    try:
        user = User.objects.get(email=request.session['email'])
        if user.usertype == "seller":
            return render(request, 'seller_index.html')
        else:
            return render(request, 'index.html')
    except:
        return render(request, 'index.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        CONTACT.objects.create(name=name, email=email, message=message)
        msg = "Feedback Saved Successfully"
        contact = CONTACT.objects.all().order_by('-id')[:10]
        return render(request, "contact.html", {"msg": msg, "contact": contact})
    else:
        contact = CONTACT.objects.all().order_by('-id')[:10]
        return render(request, 'contact.html')


def seller_register(request):
    if request.method == "POST":
        u = request.POST['username']
        e = request.POST['email']
        m = request.POST['mobile']
        p = request.POST['password']
        cp = request.POST['cpassword']
        ut = request.POST['usertype']

        try:
            user = User.objects.get(email=e)
            if user:
                msg = "Email Adress Already Registered"
                return render(request, "seller_register.html", {"msg": msg})
        except:
            if p == cp:
                User.objects.create(username=u, email=e,
                                    mobile=m, password=p, cpassword=cp, usertype=ut)
                msg = "Account Created Successfully"
                return render(request, "seller_login.html", {'email': e, 'username': u, 'msg': msg})
            else:
                msg = "Password & Confirm Password Doesn't Matched"
                return render(request, 'seller_register.html', {'msg': msg})
    return render(request, "seller_register.html")


def register(request):
    if request.method == "POST":
        u = request.POST['username']
        e = request.POST['email']
        m = request.POST['mobile']
        p = request.POST['password']
        cp = request.POST['cpassword']
        ut = request.POST['usertype']

        try:
            user = User.objects.get(email=e)
            if user:
                msg = "Email Adress Already Registered"
                return render(request, "register.html", {"msg": msg})
        except:
            if p == cp:
                User.objects.create(username=u, email=e,
                                    mobile=m, password=p, cpassword=cp, usertype=ut)
                msg = "Account Created Successfully"
                return render(request, "login.html", {'email': e, 'username': u, 'msg': msg})
            else:
                msg = "Password & Confirm Password Doesn't Matched"
                return render(request, 'register.html', {'msg': msg})
    else:
        return render(request, 'register.html')


def seller_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        usertype = request.POST['usertype']

        try:
            user = User.objects.get(
                email=email, password=password, usertype=usertype)
            request.session['username'] = user.username
            request.session['email'] = user.email
            return render(request, "seller_index.html")
        except:
            msg = "Email or Password Incorrect"
            return render(request, "seller_login.html", {"msg": msg})
    else:
        return render(request, 'seller_login.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        usertype = request.POST['usertype']

        try:
            user = User.objects.get(
                email=email, password=password, usertype=usertype)
            request.session['username'] = user.username
            request.session['email'] = user.email
            wishlists = WISHLIST.objects.filter(user=user)
            request.session['total_wishlist'] = len(wishlists)
            carts = CART.objects.filter(user=user)
            request.session['total_cart'] = len(carts)
            # checkout = CHECKOUT.objects.get(all)
            
            return render(request, "index.html")
        except:
            msg = "Email or Password Incorrect"
            return render(request, "login.html", {"msg": msg})
    else:
        return render(request, 'login.html')


def seller_logout(request):
    try:
        del request.session['seller_username']
        del request.session['seller_email']
        return render(request, "login.html")
    except:
        return render(request, "seller_login.html")


def logout(request):
    try:
        del request.session['username']
        del request.session['email']
        return render(request, "login.html")
    except:
        return render(request, "login.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            rec = [email,]
            subject = "OTP For Forgot Password"
            otp = random.randint(1000, 9999)
            message = "Your OTP For Forgot Password Is "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, rec)
            return render(request, "otp.html", {"email": email, "otp": otp})
        except:
            msg = "Email Doesn't Exist"
            return render(request, "enter_email.html", {"msg": msg})
    else:
        return render(request, "enter_email.html")


def validate_otp(request):
    email = request.POST['email']
    otp = request.POST['otp']
    uotp = request.POST['uotp']
    if otp == uotp:
        return render(request, 'enter_new_password.html', {"email": email})
    else:
        msg = "Enter OTP is Incorrect"
        return render(request, "otp.html")


def update_password(request):
    email = request.POST['email']
    npassword = request.POST['npassword']
    cnpassword = request.POST['cnpassword']

    if npassword == cnpassword:
        user = User.objects.get(email=email)
        user.password = npassword
        user.cpassword = cnpassword
        user.save()
        msg = "Your Password Is Updated Successfully"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg = "Password & Confirm New Password is Doesn't Matched"
        return render(request, 'enter_new_password.html', {'email': email, 'msg': msg})


def change_password(request):
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        cnew_password = request.POST['cnew_password']

        user = User.objects.get(email=request.session['email'])
        if user.password == new_password:
            msg = "Your New Password is Same as Old Password"
            return render(request, 'change_password.html', {'msg': msg})
        elif user.password == old_password:
            if new_password == cnew_password:
                user.password = new_password
                user.cpassword = cnew_password
                user.save()
                return redirect('logout')
            else:
                msg = "New Password & Confirm New Password is Doesn't Matched"
                return render(request, 'change_password.html', {'msg': msg})
        else:
            msg = "Old Password Is Incorrect"
            return render(request, 'change_password.html', {'msg': msg})
    else:
        user = User.objects.get(email=request.session['email'])
        if user.usertype == "seller":
            data = "seller_header.html"
            return render(request, 'change_password.html', {'user': user, 'data': data})
        else:
            return render(request, "change_password.html", {'user': user})


def edit_profile(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']
        try:
            if request.FILES['user_image']:
                user.user_image = request.FILES['user_image']
                user.save()
                request.session['user_image'] = user.user_image.url
                if user.usertype == "user":
                    return redirect('index')
                else:
                    data = "seller_header.html"
                    return render(request, 'seller_index.html', {'data': data})
        except:
            user.save()
            if user.usertype == "user":
                return redirect('index')
            else:
                data = "seller_header.html"
                return render(request, 'seller_index.html', {'data': data})
    else:
        user = User.objects.get(email=request.session['email'])
        if user.usertype == "seller":
            data = "seller_header.html"
            return render(request, 'edit_profile.html', {'user': user, 'data': data})
        else:
            return render(request, "edit_profile.html", {'user': user})


def my_account(request):
    user = User.objects.get(email=request.session['email'])
    if user.usertype == "seller":
        data = "seller_header.html"
        return render(request, "my_account.html", {'user': user, 'data': data})
    else:
        return render(request, "my_account.html", {'user': user})


def seller_index(request):
    return render(request, 'seller_index.html')

# ADD Women Cloths


def add_women_cloths(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        wc = request.POST['women_cloth_category']
        wn = request.POST['women_cloth_name']
        wp = request.POST['women_cloth_price']
        wb = request.POST['women_cloth_brand']
        wpID = request.POST['women_cloth_proID']
        wd = request.POST['women_cloth_desc']
        wi = request.FILES['women_cloth_image']
        wi1 = request.FILES['women_cloth_image1']
        wi2 = request.FILES['women_cloth_image2']
        wi3 = request.FILES['women_cloth_image3']
        wcs = request.POST.getlist('women_cloth_size')

        women_cloths = WOMEN_CLOTH.objects.filter(user=user)
        for w in women_cloths:
            if w.women_cloth_name.lower() == wn.lower():
                msg = "Cloth is Already in Your List"
                return render(request, "women_cloth/add_women_cloths.html", {'msg': msg})
        else:
            WOMEN_CLOTH.objects.create(women_cloth_category=wc, women_cloth_name=wn, women_cloth_price=wp,
                                       women_cloth_brand=wb, women_cloth_desc=wd, women_cloth_image=wi,women_cloth_image1=wi1,women_cloth_image2=wi2,women_cloth_image3=wi3, women_cloth_size=wcs, women_cloth_proID=wpID, user=user)
            msg = "Cloth Added Successfully"
            return render(request, "women_cloth/add_women_cloths.html", {'msg': msg})
    else:
        return render(request, 'women_cloth/add_women_cloths.html')

# ADD Men Cloths


def add_men_cloths(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        mc = request.POST['men_cloth_category']
        mn = request.POST['men_cloth_name']
        mp = request.POST['men_cloth_price']
        mb = request.POST['men_cloth_brand']
        md = request.POST['men_cloth_desc']
        mi = request.FILES['men_cloth_image']
        mi1 = request.FILES['men_cloth_image1']
        mi2 = request.FILES['men_cloth_image2']
        mi3 = request.FILES['men_cloth_image3']
        mcpID = request.POST['men_cloth_proID']
        mcs = request.POST.getlist('men_cloth_size')

        men_cloths = MEN_CLOTH.objects.filter(user=user)
        for m in men_cloths:
            if m.men_cloth_name.lower() == mn.lower():
                msg = "Cloth is Already in Your List"
                return render(request, "men_cloth/add_men_cloths.html", {'msg': msg})
        else:
            MEN_CLOTH.objects.create(men_cloth_category=mc, men_cloth_name=mn, men_cloth_price=mp,
                                     men_cloth_brand=mb, men_cloth_desc=md, men_cloth_image=mi,men_cloth_image1=mi1,men_cloth_image2=mi2,men_cloth_image3=mi3, men_cloth_size=mcs, men_cloth_proID=mcpID, user=user)
            msg = "Cloth Added Successfully"
            return render(request, "men_cloth/add_men_cloths.html", {'msg': msg})
    else:
        return render(request, "men_cloth/add_men_cloths.html")


# View Women Cloth Functions

def view_top(request):
    user = User.objects.get(email=request.session['email'])
    women_cloth = WOMEN_CLOTH.objects.filter(
        user=user, women_cloth_category="top")
    return render(request, 'women_cloth/view_top.html', {'women_cloth': women_cloth})


def view_pant(request):
    user = User.objects.get(email=request.session['email'])
    women_cloth = WOMEN_CLOTH.objects.filter(
        user=user, women_cloth_category="pants")
    return render(request, 'women_cloth/view_pant.html', {'women_cloth': women_cloth})


def view_saree(request):
    user = User.objects.get(email=request.session['email'])
    women_cloth = WOMEN_CLOTH.objects.filter(
        user=user, women_cloth_category="saree")
    return render(request, 'women_cloth/view_saree.html', {'women_cloth': women_cloth})


def view_punjabi(request):
    user = User.objects.get(email=request.session['email'])
    women_cloth = WOMEN_CLOTH.objects.filter(
        user=user, women_cloth_category="punjabi")
    return render(request, 'women_cloth/view_punjabi.html', {'women_cloth': women_cloth})


def view_western(request):
    user = User.objects.get(email=request.session['email'])
    women_cloth = WOMEN_CLOTH.objects.filter(
        user=user, women_cloth_category="western")
    return render(request, 'women_cloth/view_western.html', {'women_cloth': women_cloth})


def wc_product_detail(request,pk):
    women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    return render(request, 'women_cloth/wc_product_detail.html', {'women_cloth': women_cloth})


def wc_stock_avaibility(request, pk):
    women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
    if women_cloth.women_cloth_stock == "Available":
        women_cloth.women_cloth_stock = "Unavailable"
        women_cloth.save()
    else:
        women_cloth.women_cloth_stock = "Available"
        women_cloth.save()
    return redirect('wc_product_detail', pk)


def wc_delete(request, pk):
    women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
    women_cloth.delete()
    return redirect('seller_index')


def wc_edit(request, pk):
    if request.method == "POST":
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        women_cloth.women_cloth_name = request.POST['women_cloth_name']
        women_cloth.women_cloth_price = request.POST['women_cloth_price']
        women_cloth.women_cloth_brand = request.POST['women_cloth_brand']
        women_cloth.women_cloth_proID = request.POST['women_cloth_proID']
        women_cloth.women_cloth_desc = request.POST['women_cloth_desc']
        try:
            if request.FILES['women_cloth_image']:
                women_cloth.women_cloth_image = request.FILES['women_cloth_image']
                women_cloth.save()
               
        except:
            pass
        try:
            if request.FILES['women_cloth_image1']:
                women_cloth.women_cloth_image1 = request.FILES['women_cloth_image1']
                women_cloth.save()
               
        except:
            pass
        try:
            if request.FILES['women_cloth_image2']:
                women_cloth.women_cloth_image2 = request.FILES['women_cloth_image2']
                women_cloth.save()
               
        except:
            pass
        try:

            if request.FILES['women_cloth_image3']:
                women_cloth.women_cloth_image3 = request.FILES['women_cloth_image3']
                women_cloth.save()
                
        except:
            pass
        women_cloth.save()
        return redirect('seller_index')
    else:
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        return render(request, 'women_cloth/wc_edit.html', {'women_cloth': women_cloth})


# View Men Cloth Functions

def view_shirt(request):
    user = User.objects.get(email=request.session['email'])
    men_cloth = MEN_CLOTH.objects.filter(user=user, men_cloth_category="shirt")
    return render(request, 'men_cloth/view_shirt.html', {'men_cloth': men_cloth})


def view_tshirt(request):
    user = User.objects.get(email=request.session['email'])
    men_cloth = MEN_CLOTH.objects.filter(
        user=user, men_cloth_category="t-shirt")
    return render(request, 'men_cloth/view_tshirt.html', {'men_cloth': men_cloth})


def view_jeans(request):
    user = User.objects.get(email=request.session['email'])
    men_cloth = MEN_CLOTH.objects.filter(user=user, men_cloth_category="jeans")
    return render(request, 'men_cloth/view_jeans.html', {'men_cloth': men_cloth})


def view_jackets(request):
    user = User.objects.get(email=request.session['email'])
    men_cloth = MEN_CLOTH.objects.filter(
        user=user, men_cloth_category="jackets")
    return render(request, 'men_cloth/view_jackets.html', {'men_cloth': men_cloth})


def view_casual(request):
    user = User.objects.get(email=request.session['email'])
    men_cloth = MEN_CLOTH.objects.filter(
        user=user, men_cloth_category="casual")
    return render(request, 'men_cloth/view_casual.html', {'men_cloth': men_cloth})


def mc_product_detail(request, pk):
    men_cloth = MEN_CLOTH.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    return render(request, 'men_cloth/mc_product_detail.html', {'men_cloth': men_cloth})


def mc_delete(request, pk):
    men_cloth = MEN_CLOTH.objects.get(pk=pk)
    men_cloth.delete()
    return redirect('seller_index')


def mc_stock_avaibility(request, pk):
    men_cloth = MEN_CLOTH.objects.get(pk=pk)
    if men_cloth.men_cloth_stock == "Available":
        men_cloth.men_cloth_stock = "Unavailable"
        men_cloth.save()
    else:
        men_cloth.men_cloth_stock = "Available"
        men_cloth.save()
    return redirect('mc_product_detail', pk)


def mc_edit(request, pk):
    if request.method == "POST":
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        men_cloth.men_cloth_name = request.POST['men_cloth_name']
        men_cloth.men_cloth_price = request.POST['men_cloth_price']
        men_cloth.men_cloth_brand = request.POST['men_cloth_brand']
        men_cloth.men_cloth_desc = request.POST['men_cloth_desc']
        men_cloth.men_cloth_proID = request.POST['men_cloth_proID']
        try:
            if request.FILES['men_cloth_image']:
                men_cloth.men_cloth_image = request.FILES['men_cloth_image']
                men_cloth.save()
               
        except:
            pass
        try:
            if request.FILES['men_cloth_image1']:
                men_cloth.men_cloth_image1 = request.FILES['men_cloth_image1']
                men_cloth.save()
               
        except:
            pass
        try:
            if request.FILES['men_cloth_image2']:
                men_cloth.men_cloth_image2 = request.FILES['men_cloth_image2']
                men_cloth.save()
               
        except:
            pass

        try:
            if request.FILES['men_cloth_image3']:
                men_cloth.men_cloth_image3 = request.FILES['men_cloth_image3']
                men_cloth.save()
                
        except:
            pass
        men_cloth.save()
        return redirect('seller_index')
    else:
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        return render(request, 'men_cloth/mc_edit.html', {'men_cloth': men_cloth})

# ADD Women Accessories


def add_women_acc(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session['email'])
        wac = request.POST['women_acc_category']
        wan = request.POST['women_acc_name']
        wap = request.POST['women_acc_price']
        wab = request.POST['women_acc_brand']
        wad = request.POST['women_acc_desc']
        wapID = request.POST['women_acc_proID']
        wai = request.FILES['women_acc_image']
        wai1 = request.FILES['women_acc_image1']
        wai2 = request.FILES['women_acc_image2']
        wai3 = request.FILES['women_acc_image3']

        women_accs = WOMEN_ACCESSORIES.objects.filter(user=user)
        for wa in women_accs:
            if wa.women_acc_name.lower() == wan.lower():
                msg = "Accesory is Already in Your List"
                return render(request, "women_acc/add_women_acc.html", {'msg': msg})
        else:
            WOMEN_ACCESSORIES.objects.create(women_acc_category=wac, women_acc_name=wan, women_acc_price=wap,
                                             women_acc_brand=wab, women_acc_desc=wad, women_acc_image=wai,women_acc_image1=wai1,women_acc_image2=wai2,women_acc_image3=wai,women_acc_proID=wapID, user=user)
            msg = "Accesory Added Successfully"
            return render(request, "women_acc/add_women_acc.html", {'msg': msg})
    else:
        return render(request, 'women_acc/add_women_acc.html')

# View Women Accessories Function


def view_sunglasses(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="sunglasses")
    return render(request, 'women_acc/view_sunglasses.html', {'women_accs': women_accs})


def view_necklace(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="necklace")
    return render(request, 'women_acc/view_necklace.html', {'women_accs': women_accs})


def view_watch(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="watch")
    return render(request, 'women_acc/view_watch.html', {'women_accs': women_accs})


def view_tie(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="tie")
    return render(request, 'women_acc/view_tie.html', {'women_accs': women_accs})


def view_purse(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="purse")
    return render(request, 'women_acc/view_purse.html', {'women_accs': women_accs})


def view_ring(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="ring")
    return render(request, 'women_acc/view_ring.html', {'women_accs': women_accs})


def view_hairband(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="hair_band")
    return render(request, 'women_acc/view_hairband.html', {'women_accs': women_accs})


def view_cap(request):
    user = User.objects.get(email=request.session['email'])
    women_accs = WOMEN_ACCESSORIES.objects.filter(
        user=user, women_acc_category="cap")
    return render(request, 'women_acc/view_cap.html', {'women_accs': women_accs})


def wa_product_detail(request, pk):
    women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    return render(request, 'women_acc/wa_product_detail.html', {'women_acc': women_acc})


def wa_delete(request, pk):
    women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
    women_acc.delete()
    return redirect('seller_index')


def wa_stock_avaibility(request, pk):
    women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
    if women_acc.women_acc_stock == "Available":
        women_acc.women_acc_stock = "Unavailable"
        women_acc.save()
    else:
        women_acc.women_acc_stock = "Available"
        women_acc.save()
    return redirect('wa_product_detail', pk)


def wa_edit(request, pk):
    if request.method == "POST":
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        women_acc.women_acc_name = request.POST['women_acc_name']
        women_acc.women_acc_price = request.POST['women_acc_price']
        women_acc.women_acc_brand = request.POST['women_acc_brand']
        women_acc.women_acc_desc = request.POST['women_acc_desc']
        try:
            if request.FILES['women_acc_image']:
                women_acc.women_acc_image = request.FILES['women_acc_image']
                women_acc.save()
               
        except:
            pass
        try:
            if request.FILES['women_acc_image1']:
                women_acc.women_acc_image1 = request.FILES['women_acc_image1']
                women_acc.save()
               
        except:
            pass
        try:
            if request.FILES['women_acc_image2']:
                women_acc.women_acc_image2 = request.FILES['women_acc_image2']
                women_acc.save()
               
        except:
            pass
        try:

            if request.FILES['women_acc_image3']:
                women_acc.women_acc_image3 = request.FILES['women_acc_image3']
                women_acc.save()
                
        except:
            pass
        women_acc.save()
        return redirect('seller_index')
    else:
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        return render(request, 'women_acc/wa_edit.html', {'women_acc': women_acc})


# ADD Men Accessories

def add_men_acc(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session['email'])
        mac = request.POST['men_acc_category']
        man = request.POST['men_acc_name']
        map = request.POST['men_acc_price']
        mab = request.POST['men_acc_brand']
        mad = request.POST['men_acc_desc']
        mai = request.FILES['men_acc_image']
        mai1 = request.FILES['men_acc_image1']
        mai2 = request.FILES['men_acc_image2']
        mai3 = request.FILES['men_acc_image3']
        mapID = request.FILES['men_acc_proID']

        men_accs = MEN_ACCESSORIES.objects.filter(user=user)
        for ma in men_accs:
            if ma.men_acc_name.lower() == man.lower():
                msg = "Accesory is Already in Your List"
                return render(request, "men_acc/add_men_acc.html", {'msg': msg})
        else:
            MEN_ACCESSORIES.objects.create(men_acc_category=mac, men_acc_name=man, men_acc_price=map,
                                           men_acc_brand=mab, men_acc_desc=mad,men_acc_proID=mapID, men_acc_image=mai, men_acc_image1=mai1, men_acc_image2=mai2, men_acc_image3=mai3, user=user)
            msg = "Accesory Added Successfully"
            return render(request, "men_acc/add_men_acc.html", {'msg': msg})
    else:
        return render(request, 'men_acc/add_men_acc.html')

# View Men Accessories Function


def view_m_sunglasses(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="m_sunglasses")
    return render(request, 'men_acc/view_m_sunglasses.html', {'men_accs': men_accs})


def view_suspenders(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="suspenders")
    return render(request, 'men_acc/view_suspenders.html', {'men_accs': men_accs})


def view_m_watch(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="m_watch")
    return render(request, 'men_acc/view_m_watch.html', {'men_accs': men_accs})


def view_m_tie(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="m_tie")
    return render(request, 'men_acc/view_m_tie.html', {'men_accs': men_accs})


def view_m_purse(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="m_purse")
    return render(request, 'men_acc/view_m_purse.html', {'men_accs': men_accs})


def view_belt(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="belt")
    return render(request, 'men_acc/view_belt.html', {'men_accs': men_accs})


def view_socks(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="socks")
    return render(request, 'men_acc/view_socks.html', {'men_accs': men_accs})


def view_m_cap(request):
    user = User.objects.get(email=request.session['email'])
    men_accs = MEN_ACCESSORIES.objects.filter(
        user=user, men_acc_category="m_cap")
    return render(request, 'men_acc/view_m_cap.html', {'men_accs': men_accs})


def ma_product_detail(request, pk):
    men_accs = MEN_ACCESSORIES.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    return render(request, 'men_acc/ma_product_detail.html', {'men_accs': men_accs})


def ma_delete(request, pk):
    men_accs = MEN_ACCESSORIES.objects.get(pk=pk)
    men_accs.delete()
    return redirect('seller_index')


def ma_stock_avaibility(request, pk):
    men_accs = MEN_ACCESSORIES.objects.get(pk=pk)
    if men_accs.men_acc_stock == "Available":
        men_accs.men_acc_stock = "Unavailable"
        men_accs.save()
    else:
        men_accs.men_acc_stock = "Available"
        men_accs.save()
    return redirect('ma_product_detail', pk)


def ma_edit(request, pk):
    if request.method == "POST":
        men_accs = MEN_ACCESSORIES.objects.get(pk=pk)
        men_accs.men_acc_name = request.POST['men_acc_name']
        men_accs.men_acc_price = request.POST['men_acc_price']
        men_accs.men_acc_brand = request.POST['men_acc_brand']
        men_accs.men_acc_desc = request.POST['men_acc_desc']
        try:
            if request.FILES['men_acc_image']:
                men_accs.men_acc_image = request.FILES['men_acc_image']
                men_accs.save()
               
        except:
            pass
        try:
            if request.FILES['men_acc_image1']:
                men_accs.men_acc_image1 = request.FILES['men_acc_image1']
                men_accs.save()
               
        except:
            pass
        try:
            if request.FILES['men_acc_image2']:
                men_accs.men_acc_image2 = request.FILES['men_acc_image2']
                men_accs.save()
               
        except:
            pass
        try:

            if request.FILES['men_acc_image3']:
                men_accs.men_acc_image3 = request.FILES['men_acc_image3']
                men_accs.save()
                
        except:
            pass
        men_accs.save()
        return redirect('seller_index')
            
    else:
        men_accs = MEN_ACCESSORIES.objects.get(pk=pk)
        return render(request, 'men_acc/ma_edit.html', {'men_accs': men_accs})

# SEARCH ITEM


def search_item(request):
    user = User.objects.get(email=request.session['email'])
    search = request.POST['search']
    item = WOMEN_CLOTH.objects.filter(
        women_cloth_name__contains=search, user=user)
    item1 = MEN_CLOTH.objects.filter(
        men_cloth_name__contains=search, user=user)
    item2 = WOMEN_ACCESSORIES.objects.filter(
        women_acc_name__contains=search, user=user)
    if user.usertype == "seller":    
        return render(request, 'search_item.html', {'item': item, 'item1': item1, 'item2': item2})
    else:
        data = 'header.html'
        return render(request, 'search_item.html', {'item': item, 'item1': item1, 'item2': item2,'data':data})    


# ADD Women FOotwear Function

def add_women_footwear(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session['email'])
        wfc = request.POST['women_footwear_category']
        wfn = request.POST['women_footwear_name']
        wfp = request.POST['women_footwear_price']
        wfb = request.POST['women_footwear_brand']
        wfd = request.POST['women_footwear_desc']
        wfi = request.FILES['women_footwear_image']
        wfi1 = request.FILES['women_footwear_image1']
        wfi2 = request.FILES['women_footwear_image2']
        wfi3 = request.FILES['women_footwear_image3']
        wfpID = request.POST['women_footwear_proID']
        wfs = request.POST.getlist('women_footwear_size')

        women_footwear = WOMEN_FOOTWEAR.objects.filter(user=user)
        for wf in women_footwear:
            if wf.women_footwear_name.lower() == wfn.lower():
                msg = "Footwear is Already in Your List"
                return render(request, "women_footwear/add_women_footwear.html", {'msg': msg})
        else:
            WOMEN_FOOTWEAR.objects.create(women_footwear_category=wfc, women_footwear_name=wfn, women_footwear_price=wfp,
                                          women_footwear_brand=wfb, women_footwear_desc=wfd, women_footwear_image=wfi,women_footwear_image1=wfi1,women_footwear_image2=wfi2,women_footwear_image3=wfi3, women_footwear_size=wfs, women_footwear_proID=wfpID, user=user)
            msg = "Footwear Added Successfully"
            return render(request, "women_footwear/add_women_footwear.html", {'msg': msg})
    else:
        return render(request, 'women_footwear/add_women_footwear.html')

# View Women Footwear Function


def view_wedges(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="wedges")
    return render(request, 'women_footwear/view_wedges.html', {'women_footwear': women_footwear})


def view_ballerinas(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="ballerinas")
    return render(request, 'women_footwear/view_ballerinas.html', {'women_footwear': women_footwear})


def view_canvas_shoes(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="canvas_shoes")
    return render(request, 'women_footwear/view_canvas_shoes.html', {'women_footwear': women_footwear})


def view_wellington_boots(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="wellington_boots")
    return render(request, 'women_footwear/view_wellington_boots.html', {'women_footwear': women_footwear})


def view_flip_flop(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="flip_flop")
    return render(request, 'women_footwear/view_flip_flop.html', {'women_footwear': women_footwear})


def view_sandals(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="sandals")
    return render(request, 'women_footwear/view_sandals.html', {'women_footwear': women_footwear})


def view_sport_shoes(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="sport_shoes")
    return render(request, 'women_footwear/view_sport_shoes.html', {'women_footwear': women_footwear})


def view_heels(request):
    user = User.objects.get(email=request.session['email'])
    women_footwear = WOMEN_FOOTWEAR.objects.filter(
        user=user, women_footwear_category="heels")
    return render(request, 'women_footwear/view_heels.html', {'women_footwear': women_footwear})


def wf_product_detail(request, pk):
    women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    return render(request, 'women_footwear/wf_product_detail.html', {'women_footwear': women_footwear})


def wf_delete(request, pk):
    women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
    women_footwear.delete()
    return redirect('seller_index')


def wf_stock_avaibility(request, pk):
    women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
    if women_footwear.women_footwear_stock == "Available":
        women_footwear.women_footwear_stock = "Unavailable"
        women_footwear.save()
    else:
        women_footwear.women_footwear_stock = "Available"
        women_footwear.save()
    return redirect('wf_product_detail', pk)


def wf_edit(request, pk):
    if request.method == "POST":
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        women_footwear.women_footwear_name = request.POST['women_footwear_name']
        women_footwear.women_footwear_price = request.POST['women_footwear_price']
        women_footwear.women_footwear_brand = request.POST['women_footwear_brand']
        women_footwear.women_footwear_desc = request.POST['women_footwear_desc']
        women_footwear.women_footwear_proID = request.POST['women_footwear_proID']
        try:
            if request.FILES['women_footwear_image']:
                women_footwear.women_footwear_image = request.FILES['women_footwear_image']
                women_footwear.save()
               
        except:
            pass
        try:
            if request.FILES['women_footwear_image1']:
                women_footwear.women_footwear_image1 = request.FILES['women_footwear_image1']
                women_footwear.save()
               
        except:
            pass
        try:
            if request.FILES['women_footwear_image2']:
                women_footwear.women_footwear_image2 = request.FILES['women_footwear_image2']
                women_footwear.save()
               
        except:
            pass
        try:

            if request.FILES['women_footwear_image3']:
                women_footwear.women_footwear_image3 = request.FILES['women_footwear_image3']
                women_footwear.save()
                
        except:
            pass
        women_footwear.save()
        return redirect('seller_index')
    else:
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        return render(request, 'women_footwear/wf_edit.html', {'women_footwear': women_footwear})

# ADD Women FOotwear Function


def add_men_footwear(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session['email'])
        mfc = request.POST['men_footwear_category']
        mfn = request.POST['men_footwear_name']
        mfp = request.POST['men_footwear_price']
        mfb = request.POST['men_footwear_brand']
        mfd = request.POST['men_footwear_desc']
        mfi = request.FILES['men_footwear_image']
        mfi1 = request.FILES['men_footwear_image1']
        mfi2 = request.FILES['men_footwear_image2']
        mfi3 = request.FILES['men_footwear_image3']
        mfpID = request.POST['men_footwear_proID']
        mfs = request.POST.getlist('men_footwear_size')

        men_footwear = MEN_FOOTWEAR.objects.filter(user=user)
        for mf in men_footwear:
            if mf.men_footwear_name.lower() == mfn.lower():
                msg = "Footwear is Already in Your List"
                return render(request, "men_footwear/add_men_footwear.html", {'msg': msg})
        else:
            MEN_FOOTWEAR.objects.create(men_footwear_category=mfc, men_footwear_name=mfn, men_footwear_price=mfp,
                                        men_footwear_brand=mfb, men_footwear_desc=mfd, men_footwear_image=mfi,men_footwear_image1=mfi1,men_footwear_image2=mfi2,men_footwear_image3=mfi3, mf_size=mfs, men_footwear_proID=mfpID, user=user)
            msg = "Footwear Added Successfully"
            return render(request, "men_footwear/add_men_footwear.html", {'msg': msg})
    else:
        return render(request, 'men_footwear/add_men_footwear.html')

# View Men Footwear Function


def view_m_sandals(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="m_sandals")
    return render(request, 'men_footwear/view_m_sandals.html', {'men_footwear': men_footwear})


def view_m_flipflop(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="m_flipflop")
    return render(request, 'men_footwear/view_m_flipflop.html', {'men_footwear': men_footwear})


def view_m_canvas_shoes(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="m_canvas_shoes")
    return render(request, 'men_footwear/view_m_canvas_shoes.html', {'men_footwear': men_footwear})


def view_brogues(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="brogues")
    return render(request, 'men_footwear/view_brogues.html', {'men_footwear': men_footwear})


def view_oxford(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="oxford")
    return render(request, 'men_footwear/view_oxford.html', {'men_footwear': men_footwear})


def view_loafers(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="loafers")
    return render(request, 'men_footwear/view_loafers.html', {'men_footwear': men_footwear})


def view_m_sport_shoes(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="m_sport_shoes")
    return render(request, 'men_footwear/view_m_sport_shoes.html', {'men_footwear': men_footwear})


def view_leather(request):
    user = User.objects.get(email=request.session['email'])
    men_footwear = MEN_FOOTWEAR.objects.filter(
        user=user, men_footwear_category="leather")
    return render(request, 'men_footwear/view_leather.html', {'men_footwear': men_footwear})


def mf_product_detail(request, pk):
    men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    return render(request, 'men_footwear/mf_product_detail.html', {'men_footwear': men_footwear})


def mf_delete(request, pk):
    men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
    men_footwear.delete()
    return redirect('seller_index')


def mf_stock_avaibility(request, pk):
    men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
    if men_footwear.men_footwear_stock == "Available":
        men_footwear.men_footwear_stock = "Unavailable"
        men_footwear.save()
    else:
        men_footwear.men_footwear_stock = "Available"
        men_footwear.save()
    return redirect('mf_product_detail', pk)


def mf_edit(request, pk):
    if request.method == "POST":
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        men_footwear.men_footwear_name = request.POST['men_footwear_name']
        men_footwear.men_footwear_price = request.POST['men_footwear_price']
        men_footwear.men_footwear_brand = request.POST['men_footwear_brand']
        men_footwear.men_footwear_desc = request.POST['men_footwear_desc']
        men_footwear.men_footwear_proID = request.POST['men_footwear_proID']
        try:
            if request.FILES['men_footwear_image']:
                men_footwear.men_footwear_image = request.FILES['men_footwear_image']
                men_footwear.save()
               
        except:
            pass
        try:
            if request.FILES['men_footwear_image1']:
                men_footwear.men_footwear_image1 = request.FILES['men_footwear_image1']
                men_footwear.save()
               
        except:
            pass
        try:
            if request.FILES['men_footwear_image2']:
                men_footwear.men_footwear_image2 = request.FILES['men_footwear_image2']
                men_footwear.save()
               
        except:
            pass
        try:

            if request.FILES['men_footwear_image3']:
                men_footwear.men_footwear_image3 = request.FILES['men_footwear_image3']
                men_footwear.save()
                
        except:
            pass
        men_footwear.save()
        return redirect('seller_index')
    else:
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        return render(request, 'men_footwear/mf_edit.html', {'men_footwear': men_footwear})

# Buyer Side


def show_w_cloths(request, cn):
    w_cloths = WOMEN_CLOTH.objects.filter(women_cloth_category__contains=cn)
    return render(request, 'women_cloth/buyer_side/show_w_cloths.html', {'w_cloths': w_cloths})


def user_wc_detail(request, pk):
    flag = False
    flag1 = False
    women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
    # user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(women_cloth=women_cloth)
    carts = CART.objects.filter(women_cloth=women_cloth)
    for i in wishlists:
        if i.women_cloth.pk == women_cloth.pk:
            flag = True
            break
    for i in carts:
        if i.women_cloth.pk == women_cloth.pk:
            flag1 = True
            break
    return render(request, 'women_cloth/buyer_side/user_wc_detail.html', {'women_cloth': women_cloth, 'flag': flag, 'flag1': flag1})


def show_m_cloths(request, sc):
    m_cloths = MEN_CLOTH.objects.filter(men_cloth_category__contains=sc)
    return render(request, 'men_cloth/mc_buyer_side/show_m_cloths.html', {'m_cloths': m_cloths})


def user_mc_detail(request, pk):
    flag = False
    flag1 = False
    men_cloth = MEN_CLOTH.objects.get(pk=pk)
    # user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(men_cloth=men_cloth)
    carts = CART.objects.filter(men_cloth=men_cloth)
    for i in wishlists:
        if i.men_cloth.pk == men_cloth.pk:
            flag = True
            break
    for i in carts:
        if i.men_cloth.pk == men_cloth.pk:
            flag1 = True
            break
    return render(request, 'men_cloth/mc_buyer_side/user_mc_detail.html', {'men_cloth': men_cloth, 'flag': flag, 'flag1': flag1})


def show_w_acc(request, sa):
    w_acc = WOMEN_ACCESSORIES.objects.filter(women_acc_category__contains=sa)
    return render(request, 'women_acc/wa_buyer_side/show_w_acc.html', {'w_acc': w_acc})


def user_wa_detail(request, pk):
    flag = False
    flag1 = False
    women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
    # user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(women_acc=women_acc)
    carts = CART.objects.filter(women_acc=women_acc)
    for i in wishlists:
        if i.women_acc.pk == women_acc.pk:
            flag = True
            break
    for i in carts:
        if i.women_acc.pk == women_acc.pk:
            flag1 = True
            break
    return render(request, 'women_acc/wa_buyer_side/user_wa_detail.html', {'women_acc': women_acc, 'flag': flag, 'flag1': flag1})


def show_m_acc(request, sa):
    m_acc = MEN_ACCESSORIES.objects.filter(men_acc_category__contains=sa)
    return render(request, 'men_acc/ma_buyer_side/show_m_acc.html', {'m_acc': m_acc})


def user_ma_detail(request, pk):
    flag = False
    flag1 = False
    men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
    # user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(men_acc=men_acc)
    carts = CART.objects.filter(men_acc=men_acc)
    for i in wishlists:
        if i.men_acc.pk == men_acc.pk:
            flag = True
            break
    for i in carts:
        if i.men_acc.pk == men_acc.pk:
            flag1 = True
            break
    return render(request, 'men_acc/ma_buyer_side/user_ma_detail.html', {'men_acc': men_acc, 'flag': flag, 'flag1': flag1})


def show_w_footwear(request, sf):
    w_footwear = WOMEN_FOOTWEAR.objects.filter(
        women_footwear_category__contains=sf)
    return render(request, 'women_footwear/wf_buyer_side/show_w_footwear.html', {'w_footwear': w_footwear})


def user_wf_detail(request, pk):
    flag = False
    flag1 = False
    women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
    # user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(women_footwear=women_footwear)
    carts = CART.objects.filter(women_footwear=women_footwear)
    for i in wishlists:
        if i.women_footwear.pk == women_footwear.pk:
            flag = True
            break
    for i in carts:
        if i.women_footwear.pk == women_footwear.pk:
            flag1 = True
            break
    return render(request, 'women_footwear/wf_buyer_side/user_wf_detail.html', {'women_footwear': women_footwear, 'flag': flag, 'flag1': flag1})


def show_m_footwear(request, sf):
    m_footwear = MEN_FOOTWEAR.objects.filter(
        men_footwear_category__contains=sf)
    return render(request, 'men_footwear/mf_buyer_side/show_m_footwear.html', {'m_footwear': m_footwear})


def user_mf_detail(request, pk):
    flag = False
    flag1 = False
    men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
    # user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(men_footwear=men_footwear)
    carts = CART.objects.filter(men_footwear=men_footwear)
    for i in wishlists:
        if i.men_footwear.pk == men_footwear.pk:
            flag = True
            break
    for i in carts:
        if i.men_footwear.pk == men_footwear.pk:
            flag1 = True
            break
    return render(request, 'men_footwear/mf_buyer_side/user_mf_detail.html', {'men_footwear': men_footwear, 'flag': flag, 'flag1': flag1})

# WISHLIST


def mywishlist(request):
    user = User.objects.get(email=request.session['email'])
    wishlists = WISHLIST.objects.filter(user=user)
    request.session['total_wishlist'] = len(wishlists)
    return render(request, 'mywishlist.html', {'wishlists': wishlists})


def add_to_wishlist(request, pk, t):
    user = User.objects.get(email=request.session['email'])
    if t == "wa":
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, women_acc=women_acc)
    elif t == "wc":
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, women_cloth=women_cloth)
    elif t == "wf":
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, women_footwear=women_footwear)
    elif t == "ma":
        men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, men_acc=men_acc)
    elif t == "mc":
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, men_cloth=men_cloth)
    elif t == "mf":
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, men_footwear=men_footwear)
    return redirect('mywishlist')


def remove_from_wishlist(request, pk, x):
    user = User.objects.get(email=request.session['email'])

    if x == 'wc':
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        wishlists = WISHLIST.objects.get(user=user, women_cloth=women_cloth)
        wishlists.delete()
    elif x == 'wa':
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        wishlists = WISHLIST.objects.get(user=user, women_acc=women_acc)
        wishlists.delete()
    elif x == 'wf':
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        wishlists = WISHLIST.objects.get(
            user=user, women_footwear=women_footwear)
        wishlists.delete()
    elif x == 'mc':
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        wishlists = WISHLIST.objects.get(user=user, men_cloth=men_cloth)
        wishlists.delete()
    elif x == 'ma':
        men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
        wishlists = WISHLIST.objects.get(user=user, men_acc=men_acc)
        wishlists.delete()
    elif x == 'mf':
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        wishlists = WISHLIST.objects.get(user=user, men_footwear=men_footwear)
        wishlists.delete()
    return redirect('mywishlist')


def move_to_wishlist(request, pk, l):
    user = User.objects.get(email=request.session['email'])

    if l == 'wc':
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, women_cloth=women_cloth)
        cart = CART.objects.get(user=user, women_cloth=women_cloth)
        cart.delete()
    elif l == 'wa':
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, women_acc=women_acc)
        cart = CART.objects.get(user=user, women_acc=women_acc)
        cart.delete()
    elif l == 'wf':
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, women_footwear=women_footwear)
        cart = CART.objects.get(user=user, women_footwear=women_footwear)
        cart.delete()
    elif l == 'mc':
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, men_cloth=men_cloth)
        cart = CART.objects.get(user=user, men_cloth=men_cloth)
        cart.delete()
    elif l == 'ma':
        men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, men_acc=men_acc)
        cart = CART.objects.get(user=user, men_acc=men_acc)
        cart.delete()
    elif l == 'mf':
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        WISHLIST.objects.create(user=user, men_footwear=men_footwear)
        cart = CART.objects.get(user=user, men_footwear=men_footwear)
        cart.delete()
    carts = CART.objects.filter(user=user)
    request.session['total_cart'] = len(carts)
    return redirect('mywishlist')

# CART


def mycart(request):
    net_price = 0
    user = User.objects.get(email=request.session['email'])
    carts = CART.objects.filter(user=user)
    for i in carts:
        net_price = net_price+i.total_price
    request.session['total_cart'] = len(carts)
    return render(request, 'mycart.html', {'carts': carts, 'net_price': net_price})


def add_to_cart(request, pk, s):
    user = User.objects.get(email=request.session['email'])
    if s == "wa":
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        CART.objects.create(user=user, women_acc=women_acc,
                            total_price=women_acc.women_acc_price, total_qty=1)
    elif s == "wc":
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        CART.objects.create(user=user, women_cloth=women_cloth,
                            total_price=women_cloth.women_cloth_price, total_qty=1)
    elif s == "wf":
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        CART.objects.create(user=user, women_footwear=women_footwear,
                            total_price=women_footwear.women_footwear_price, total_qty=1)
    elif s == "ma":
        men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
        CART.objects.create(user=user, men_acc=men_acc,
                            total_price=men_acc.men_acc_price, total_qty=1)
    elif s == "mc":
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        CART.objects.create(user=user, men_cloth=men_cloth,
                            total_price=men_cloth.men_cloth_price, total_qty=1)
    elif s == "mf":
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        CART.objects.create(user=user, men_footwear=men_footwear,
                            total_price=men_footwear.men_footwear_price, total_qty=1)
    return redirect('mycart')


def remove_from_cart(request, pk, y):
    user = User.objects.get(email=request.session['email'])

    if y == 'wc':
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        carts = CART.objects.get(user=user, women_cloth=women_cloth)
        carts.delete()
    elif y == 'wa':
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        carts = CART.objects.get(user=user, women_acc=women_acc)
        carts.delete()
    elif y == 'wf':
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        carts = CART.objects.get(user=user, women_footwear=women_footwear)
        carts.delete()
    elif y == 'mc':
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        carts = CART.objects.get(user=user, men_cloth=men_cloth)
        carts.delete()
    elif y == 'ma':
        men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
        carts = CART.objects.get(user=user, men_acc=men_acc)
        carts.delete()
    elif y == 'mf':
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        carts = CART.objects.get(user=user, men_footwear=men_footwear)
        carts.delete()
    return redirect('mycart')


def move_to_cart(request, pk, k):
    user = User.objects.get(email=request.session['email'])

    if k == 'wc':
        women_cloth = WOMEN_CLOTH.objects.get(pk=pk)
        CART.objects.create(user=user, women_cloth=women_cloth,
                            total_price=women_cloth.women_cloth_price, total_qty=1)
        wishlist = WISHLIST.objects.get(user=user, women_cloth=women_cloth)
        wishlist.delete()
    elif k == 'wa':
        women_acc = WOMEN_ACCESSORIES.objects.get(pk=pk)
        CART.objects.create(user=user, women_acc=women_acc,
                            total_price=women_acc.women_acc_price, total_qty=1)
        wishlist = WISHLIST.objects.get(user=user, women_acc=women_acc)
        wishlist.delete()
    elif k == 'wf':
        women_footwear = WOMEN_FOOTWEAR.objects.get(pk=pk)
        CART.objects.create(user=user, women_footwear=women_footwear,
                            total_price=women_footwear.women_footwear_price, total_qty=1)
        wishlist = WISHLIST.objects.get(
            user=user, women_footwear=women_footwear)
        wishlist.delete()
    elif k == 'mc':
        men_cloth = MEN_CLOTH.objects.get(pk=pk)
        CART.objects.create(user=user, men_cloth=men_cloth,
                            total_price=men_cloth.men_cloth_price, total_qty=1)
        wishlist = WISHLIST.objects.get(user=user, men_cloth=men_cloth)
        wishlist.delete()
    elif k == 'ma':
        men_acc = MEN_ACCESSORIES.objects.get(pk=pk)
        CART.objects.create(user=user, men_acc=men_acc,
                            total_price=women_acc.women_acc_price, total_qty=1)
        wishlist = WISHLIST.objects.get(user=user, men_acc=men_acc)
        wishlist.delete()
    elif k == 'mf':
        men_footwear = MEN_FOOTWEAR.objects.get(pk=pk)
        CART.objects.create(user=user, men_footwear=men_footwear,
                            total_price=women_footwear.women_footwear_price, total_qty=1)
        wishlist = WISHLIST.objects.get(user=user, men_footwear=men_footwear)
        wishlist.delete()
    wishlists = WISHLIST.objects.filter(user=user)
    request.session['total_wishlist'] = len(wishlists)
    return redirect('mycart')


def update_price(request):
    price = request.POST['price']
    qty = request.POST['qty']
    pk = request.POST['pk']
    cart = CART.objects.get(pk=pk)
    total_price = int(price)*int(qty)
    cart.total_price = total_price
    cart.total_qty = qty
    cart.save()
    return redirect("mycart")


def checkout_(request):
    net = request.POST['amount']
    size = request.POST['item_size']
    return render(request, 'checkout_.html', {'net': net,'size':size})


def checkout(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        net = request.POST['amount']
        fn = request.POST['fname']
        ln = request.POST['lname']
        email = request.POST['e_mail']
        mobile = request.POST['m_obile']
        fax = request.POST['fax']
        add1 = request.POST['add1']
        add2 = request.POST['add2']
        city = request.POST['city']
        post_code = request.POST['post_code']
        country = request.POST['country']
        state = request.POST['state']
        size = request.POST['item_size']

        CHECKOUT.objects.create(fname=fn, lname=ln, e_mail=email, m_obile=mobile, fax=fax, add1=add1,
                                add2=add2, city=city, post_code=post_code, country=country, state=state,amount=net,item_size=size)
        msg = 'Address Added Successfully'
        return render(request, "checkout.html", {'msg': msg,'amount':net, 'fname': fn, "lname": ln, 'e_mail': email, 'm_obile': mobile, 'fax': fax, 'add1': add1, 'add2': add2,'city': city, 'post_code': post_code, 'country': country, 'state': state,'item_size': size })
    else:
        return render(request, 'checkout.html')
