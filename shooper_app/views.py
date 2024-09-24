from django.shortcuts import render, HttpResponse ,redirect
from django.conf import settings
from .models import*
import random
from django.core.mail import send_mail
from django.core.paginator import Paginator
import razorpay
from django.db.models import *

# Create your views here.




def index(request):
    if "email" in request.session:
        mid=main_category.objects.all()
        uid=User.objects.get(email=request.session['email'])  
        a_count=add_cart.objects.filter(user=uid).count()
        sid=sub_category.objects.annotate(count1=Count("count"))
        pid=product.objects.order_by("-id")[:8]
        # for i in sid:
        #     print(i.name,i.count1)
        # print(a_count)
        tid=product.objects.annotate(total=Count("top")).order_by("-total")[:2]
        print(tid)
        for i in tid:
            print(i,i.total)
        s_id=request.GET.get("s_id")
        print(s_id)
        if s_id:
            pid=product.objects.filter(sub_category=s_id)
            contaxt={
                "pid":pid
            }
            return render(request,"shop.html",contaxt)
        contaxt={
            "mid":mid,
            "pid":pid,
            "a_count":a_count,
            "uid":uid,
            "sid":sid,
        }
        return render(request,"index.html",contaxt)
    else:
        return render(request,"login.html")



def shop(request):
    
        mid=main_category.objects.all()
        # print(mid)
        # pid=product.objects.all()
        # 1 2 3
        pid=product.objects.order_by("-id")
        # print(pid)
        pfid=price_filter.objects.all()
        sfid=size_filter.objects.all()
        # print(pfid)
        pfidg=request.GET.get("pfid")
        sort=request.GET.get("sort")
        
        print(sort)

        s_id=request.GET.get("s_id")
        print(s_id)
        
        if pfidg=="all":
            pid=product.objects.order_by("-id") 
        elif s_id:
            pid=product.objects.filter(sub_category=s_id)    
            print("Sub_category : ",pid)
        elif pfidg:
            pid=product.objects.filter(price_filter=pfidg)
        
        elif sort=="atoz":    
            pid=product.objects.order_by("name")
        elif sort=="ztoa":    
            pid=product.objects.order_by("-name")    
        elif sort=="ltoh":    
            pid=product.objects.order_by("price")
        elif sort=="htol":    
            pid=product.objects.order_by("-price")        
        else:
            pid=product.objects.order_by("-id")

        paginator=Paginator(pid,5)   
        page_number=request.GET.get("page")
        pid=paginator.get_page(page_number) 

        # import requests

        # api_url = "https://api.escuelajs.co/api/v1/products"

        # response = requests.get(api_url)
        # data=response.json()
        # for i in data:
        #     print(i)
        contaxt={
            "mid":mid,
            # "data":data,
            "pid":pid,
            "pfid":pfid,
            "sfid":sfid,
        }
        return render(request,"shop.html",contaxt)
    

def cart(request):
    uid=User.objects.get(email=request.session['email'])
    cid=add_cart.objects.filter(user=uid)
    a_count=add_cart.objects.filter(user=uid).count()
    l1=[]
    sub_total=0
    shipping=10
    total=0
    for i in cid:
        l1.append(i.total)
    sub_total=sum(l1) 
    total=sub_total+shipping
    request.session['my_variable'] = 0
    contaxt={
        "cid":cid,
        "a_count":a_count,
        "sub_total":sub_total,
        "shipping":shipping,
        "total":total,
        

    }
    return render(request,"cart.html",contaxt)
def checkout(request):
    uid=User.objects.get(email=request.session['email'])
    cid=add_cart.objects.filter(user=uid)
    
    
    l1=[]
    sub_total=0
    shipping=10
    total=0
    for i in cid:
        l1.append(i.total)
    sub_total=sum(l1) 
    total=sub_total+shipping
    if request.POST:
        f_name=request.POST['f_name']
        l_name=request.POST['l_name']
        email=request.POST['email']
        phone=request.POST['phone']
        address0=request.POST['address']
        address1=request.POST['address1']
        country=request.POST['country']
        city=request.POST['city']
        pincode=request.POST['pincode']
        print(f_name,l_name,email)
        address.objects.create(user=uid,f_name=f_name,l_name=l_name,email=email,phone=phone,address0=address0,address1=address1,country=country,cite=city,pincode=pincode)
        client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))   
        response = client.order.create({'amount':total*100,'currency':'INR','payment_capture':1})
        for i in cid:
            order1.objects.create(order_id=response['id'],product=i.product,user=uid,name=i.name,img=i.img,price=i.price,qty=i.qty)
            i.delete() 
        return redirect("invoice")

    
    client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))   
    response = client.order.create({'amount':total*100,'currency':'INR','payment_capture':1})
    print(response,"**************")
        
    contaxt={
        "cid":cid,
        "sub_total":sub_total,
        "shipping":shipping,
        "total":total,
        "ch":ch,
        "uid":uid,
        "response":response,
    }
    return render(request,"checkout.html",contaxt)

def product_detail(request,id):
    pidg=product.objects.get(id=id)
    print(pidg.name)
    rid=review_details.objects.filter(product=pidg)
    rid_count=review_details.objects.filter(product=pidg).count()
    l1=[]
    for i in rid:
        l1.append(int(i.rating))
    a=sum(l1)/rid_count    
    print(a)
    contaxt={
        "pidg":pidg,
        "rid":rid,
        "a":a,
        
    }
    return render(request,"detail.html",contaxt)




def contact(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        
        Contact.objects.create(name=name,email=email,subject=subject,message=message)
    return render(request,"contact.html")



def login(request):
    if 'email'in request.session:
        return render(request,"index.html")
    try:
        if request.POST:
            email=request.POST['email']
            password=request.POST['password']
            uid=User.objects.get(email=email)
    
            if uid.email==email: 
                if uid.password==password:
                    request.session['email']=uid.email
                    return redirect("index")
                else:
                    msg = {"p_msg":"Incorrect Password 1"}
                    return render(request,"login.html",msg) 
            else:
                #msg = {"e_msg":"Incorrect Email 2"}
                return render(request,"login.html")
        else:
            return render(request,"login.html")
    except:
        msg = {"e_msg":"Incorrect Email 2"}
        return render(request,"login.html",msg)  


def register(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['c_password']

        try:
            if len(name) or len(email) or len(password) == 0:
                return render(request,'registration.html')
            
            uid=User.objects.get(email=email)
            if uid.email==email:
                con={"e_msg":"Email Already Exist !"}   # Email error messgae
                return render(request,'register.html',con)
        
        except:
            if password==c_password:
                User.objects.create(name=name, email=email, password=password)
                return render(request, 'login.html')
            else:
                con={"cp_msg":"password not match with conform password"}
                return render(request,'register.html',con)
        
    else:
        return render(request,"register.html")


# LOGOUT                       
def logout(request):
    if 'email' in request.session:
        del request.session['email']

    return render(request,'login.html')


#FORGOT
# def forget(request):
#     if request.POST:
#         email = request.POST.get('email')  #request.POST['email'].get()
#         if email:
#             otp=random.randint(1111,9999)  
#             try:
#                 otp_instance,created=User.objects.get_or_create(email=email)
#                 otp_instance.otp=otp
#                 otp_instance.save()
#                 send_mail("forget password",'your otp is : ','gohiljayb10@gmail.com',['pateldeep9662@gmail.com'], fail_silently=True,)
#                 con={"email":email}
#                 return render(request,"confirm_password.html",con)
#             except:
#                 con={"h":"hiiii"}
#                 return render(request,"forget.html",con)
#         else:
#             return render(request,"forget.html")
#     else:
#         return render(request,"forget.html")
    

def forget(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        print(email,otp)
        try:
            uid=User.objects.get(email=email)
            uid.otp=otp
            uid.save()
            send_mail("Password Change",f"Your Otp Is - {otp}","gohiljayb10@gmail.com",[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm_password.html",contaxt)
        except:
            contaxt={
                "msg":"Invalid Email"
            }    
            return render(request,"forget.html",contaxt)

    else:
        return render(request,"forget.html")

def confirm_password(request):
    if request.POST:
        email=request.POST['email1']
        otp=request.POST['otp']
        n_password=request.POST['n_password']
        c_password=request.POST['c_password']
        print(email,otp,n_password,c_password)

        uid=User.objects.get(email=email)
        print(type(uid.otp),type(otp))
        if uid.otp==int(otp):
            if n_password==c_password:
                uid.password=n_password
                uid.save()
                return redirect("login")
            else:
                contaxt={
                    "msg":"Invalid Password"
                }    
                return render(request,"confirm_password.html",contaxt)    
        else:
            contaxt={
                "msg":"Invalid OTP"
            }    
            return render(request,"confirm_password.html",contaxt)


    return render(request,"confirm_password.html")

def search_fun(request):
    search=request.GET.get("search")
    print(search)
    if search:
        pid=product.objects.filter(name__contains=search)
    contaxt={
        "pid":pid
    }    
    return render(request,"shop.html",contaxt)

def add_to_cart(request,id):
    pid=product.objects.get(id=id)
    uid=User.objects.get(email=request.session['email'])
    aid=add_cart.objects.filter(product=pid,user=uid).exists()
    print(uid)
    if aid:
        aid=add_cart.objects.get(product=pid)
        aid.qty+=1
        aid.total=aid.qty*aid.price
        aid.save()
        return redirect("cart")
    else:
        add_cart.objects.create(product=pid,user=uid,img=pid.img,name=pid.name,price=pid.price,qty=1,total=pid.price)
        return redirect("cart")


def qty_plus(request,id):
    aid=add_cart.objects.get(id=id)
    aid.qty+=1
    aid.total=aid.qty*aid.price
    aid.save()
    return redirect("cart")

def qty_minus(request,id):
    aid=add_cart.objects.get(id=id)
    aid.qty-=1
    aid.total=aid.qty*aid.price
    aid.save()
    if aid.qty==0:
        aid.delete()
    
    return redirect("cart")

def remove_cart(request,id):
    aid=add_cart.objects.get(id=id)
    aid.delete()
    return redirect("cart")

def order(request):
    oid=order1.objects.order_by("-id")[:1]
    a=None
    date=None
    for i in oid:
        a=i.order_id
        date=i.date
        print(i.order_id)
    print(a)    
    oid1=order1.objects.filter(order_id=a)
    contaxt={
        "oid":oid,
        "oid1":oid1,
        "a":a,
        
    }
    return render(request, 'order.html',contaxt)

def profile(request):
    uid=User.objects.get(email=request.session['email'])
    print(uid.name)
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        if request.FILES:
            img=request.FILES['img']
            uid.name=name
            uid.email=email
            uid.phone=phone
            uid.address1=address
            uid.img1=img
            uid.save()
        else:
            uid.name=name
            uid.email=email
            uid.phone=phone
            uid.address1=address
            uid.save()

        request.session['email']=email

    contaxt={
        "uid":uid
    }
    return render(request,"profile.html",contaxt)




def price_filter1(request):
    c1=request.GET.get("color-1")
    c2=request.GET.get("color-2")
    c3=request.GET.get("color-3")
    c4=request.GET.get("color-4")
    c5=request.GET.get("color-5")
    pid=[]
    if c1:
        print("Black")
        p=product.objects.filter(color="Black")
        pid.extend(p)
    if c2:
        print("White")
        p=product.objects.filter(color="White")
        pid.extend(p)
    if c3:
        print("Red")
        p=product.objects.filter(color="Red")
        pid.extend(p) 
    if c4:
        print("Blue")  
        p=product.objects.filter(color="Blue")
        pid.extend(p) 
    if c5:
        print("Green")  
        p=product.objects.filter(color="Green")
        pid.extend(p)
    if len(pid) == 0:
        print("ok")      
    contaxt={
        "pid":pid,
        "p_count":len(pid)
    }
    return render(request, 'shop.html',contaxt)

def size_filter1(request):
    s1=request.GET.get("size-1")
    s2=request.GET.get("size-2")
    s3=request.GET.get("size-3")
    s4=request.GET.get("size-4")
    s5=request.GET.get("size-5")
    print(s1,s2,s3,s4,s5)

    pid=product.objects.filter(Q(size_filter=s1) | Q(size_filter=s2) | Q(size_filter=s3) | Q(size_filter=s4) | Q(size_filter=s5) ).distinct()
    print(pid)
   
    contaxt={
        "pid":pid,
    }
    return render(request, 'shop.html',contaxt)


def bill(request):
    uid=User.objects.get(email=request.session['email'])
    bid=address.objects.filter(user=uid).order_by("-id")[:1]
    for i in bid:
        print(i.f_name,i.l_name)
    oid=order1.objects.order_by("-id")[:1]
    a=None
    date=None
    for i in oid:
        a=i.order_id
        date=i.date
        print(i.order_id)
    print(a)    
    oid1=order1.objects.filter(order_id=a)
    print(oid1)
    l1=[]
    sub_total=0
    for i in oid1:
        l1.append(i.price)
    sub_total=sum(l1)
    shipping=10    
    # t1=sub_total*18/100
    discount=sub_total*10/100
    my_variable = request.session.get('my_variable')
    total=sub_total+shipping-my_variable

    print("ok",my_variable)
    contaxt={
        "oid":oid,
        "bid":bid,
        "oid1":oid1,
        "a":a,
        "sub_total":sub_total,
        "shipping":shipping,
        "discount":my_variable,
        "date":date,
        "total":total,
    }
    return render(request, 'bill.html',contaxt)


def apply_coupon(request):
    uid=User.objects.get(email=request.session['email'])
    cid=add_cart.objects.filter(user=uid)
    
    
    l1=[]
    sub_total=0
    shipping=10
    total=0
    for i in cid:
        l1.append(i.total)
    sub_total=sum(l1) 
    total=sub_total+shipping
    discount=0
    if request.POST:
        coupon1=request.POST['coupon']
        coupon_id=coupon.objects.filter(code=coupon1).exists()
        print(coupon_id)
        if coupon_id:
            cid1=coupon.objects.get(code=coupon1)
            discount=cid1.discount
            total=total-cid1.discount
            request.session['my_variable'] = discount
            client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))   
            response = client.order.create({'amount':total*100,'currency':'INR','payment_capture':1})
            print(response,"**************")
            contaxt={
                "total":total,
                "sub_total":sub_total,
                "shipping":shipping,
                "cid":cid,
                "discount":discount,
                "ch":ch,
                "response":response,
            } 
            return render(request, 'checkout.html',contaxt)
    else:    
        return render(request, 'cart.html')
        
def invoice(request):
    uid=User.objects.get(email=request.session['email'])
    bid=address.objects.filter(user=uid).order_by("-id")[:1]
    for i in bid:
        print(i.f_name,i.l_name)
    oid=order1.objects.order_by("-id")[:1]
    a=None
    date=None
    for i in oid:
        a=i.order_id
        date=i.date
        print(i.order_id)
    print(a)    
    oid1=order1.objects.filter(order_id=a)
    print(oid1)
    l1=[]
    sub_total=0
    for i in oid1:
        l1.append(i.price*i.qty)
    sub_total=sum(l1)
    shipping=10    
    # t1=sub_total*18/100
    discount=sub_total*10/100
    my_variable = request.session.get('my_variable')
    total=sub_total+shipping-my_variable

    print("ok",my_variable)
    contaxt={
        "oid":oid,
        "bid":bid,
        "oid1":oid1,
        "a":a,
        "sub_total":sub_total,
        "shipping":shipping,
        "discount":my_variable,
        "date":date,
        "total":total,
    }
    return render(request, 'invoice.html',contaxt)

def single_add_to_cart(request,id):
    pid=product.objects.get(id=id)
    uid=User.objects.get(email=request.session['email'])
    aid=add_cart.objects.filter(product=pid,user=uid).exists()
    print(uid)
    if request.POST:
        qty=request.POST['qty']
        print(qty)
        
        if aid:
            aid=add_cart.objects.get(product=pid)
            aid.qty+=int(qty)
            aid.total=aid.qty*aid.price
            aid.save()
            return redirect("cart")
        else:
            qty=int(qty)
            total=qty*pid.price
            print(total)
            add_cart.objects.create(product=pid,user=uid,img=pid.img,name=pid.name,price=pid.price,qty=qty,total=total)
            return redirect("cart")
    return redirect("cart")        

def review_view(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        review = request.POST["review"]
        rating = request.POST["rate"]
        id = request.POST["id"]
        pid=product.objects.get(id=id)
        print(name, email, review, rating)
        review_details.objects.create(name=name, email=email, review=review, rating=rating,product=pid)
    return redirect("product_detail",id=id)






