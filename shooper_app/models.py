from django.db import models
import datetime

# Create your models here.

# CONTACT INFORMATION
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    subject=models.CharField(max_length=50)
    message=models.TextField()
    time=models.DateTimeField(editable=True, auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.name
    
# REGISTRATION INFORMATION        
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    time=models.DateTimeField(editable=True, auto_now_add=True)
    otp=models.IntegerField()
    img1=models.ImageField(upload_to="image",default=r"C:\Users\Parimal\OneDrive\Documents\Live Project\shopper_env\shopper_project\shooper_app\static\img\avatar6.png")
    phone=models.IntegerField(blank=True,null=True)
    address1=models.CharField(max_length=50,blank=True,null=True)
    
    
    def __str__(self):
        return self.email


# LOGIN INFORMATION
class Login(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    time=models.DateTimeField(editable=True, auto_now_add=True)
    
    def __str__(self):
        return self.email

class main_category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name



    def __str__(self):
        return self.name
        
class price_filter(models.Model):
    price=models.CharField(max_length=50)

    def __str__(self):
        return self.price

class size_filter(models.Model):
    size=models.CharField(max_length=50)

    def __str__(self):
        return self.size

class sub_category(models.Model):
    main_category=models.ForeignKey(main_category,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to="image",blank=True,null=True)

ch=(("Black","Black"),("White","White"),("Red","Red"),("Blue","Blue"),("Green","Green"))
class product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    rate=models.IntegerField(blank=True,null=True)
    img=models.ImageField(upload_to="image")
    img1=models.ImageField(upload_to="image",blank=True,null=True)
    img2=models.ImageField(upload_to="image",blank=True,null=True)
    img3=models.ImageField(upload_to="image",blank=True,null=True)
    price_filter=models.ForeignKey(price_filter,on_delete=models.CASCADE,blank=True,null=True)
    size_filter=models.ManyToManyField(size_filter,blank=True)
    sub_category=models.ForeignKey(sub_category,related_name="count",on_delete=models.CASCADE,blank=True,null=True)
    color=models.CharField(choices=ch,blank=True,null=True,max_length=50)
    def __str__(self):
        return self.name


class add_cart(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    img=models.ImageField(upload_to="image")
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    qty=models.IntegerField()
    total=models.IntegerField()
    
    def __str__(self):
        return self.name

ch=(("A","A"),("B","B"),("C","C"))
class address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    f_name=models.CharField(max_length=50)      
    l_name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.IntegerField()
    address0=models.CharField(max_length=100)      
    address1=models.CharField(max_length=100)  
    cite=models.CharField(max_length=100)
    pincode=models.IntegerField()
    country=models.CharField(choices=ch,max_length=100)
    
    def __str__(self):
        return self.f_name

class order1(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(address,on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(product,related_name="top", on_delete=models.CASCADE,blank=True,null=True)
    order_id=models.CharField(max_length=30,blank=True,null=True)
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    qty=models.IntegerField()
    img=models.ImageField(upload_to="image")
    date=models.DateField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return self.name

class coupon(models.Model):
    code=models.CharField(max_length=5)
    discount=models.IntegerField(default=100)

    def __str__(self):
        return self.code


class review_details(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    review=models.TextField(max_length=500)
    rating=models.CharField(max_length=10,choices=[(i,i) for i in range(1,6)])
    date=models.DateTimeField(auto_now=True)
    product=models.ForeignKey(product, on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.name




