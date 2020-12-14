from django.db import models
from django.utils import timezone
# from multiselectfield import MultiSelectField
# Create your models here.

# USER MODEL

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    cpassword = models.CharField(max_length=100)
    user_image = models.ImageField(upload_to="user_images/",default="user.png")
    usertype = models.CharField(max_length=50,default='user')
    
    def __str__(self):
        return self.username.upper()

# CONTACT MODEL

class CONTACT(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# WOMEN CLOTH MODEL

class WOMEN_CLOTH(models.Model):
    CHOICE = ( 
        ("top",'top'),
        ("pants",'pants'),
        ("Saree",'saree'),
        ("punjabi",'punjabi'),
        ("western",'western'),
    )

    women_cloth_category = models.CharField(max_length=100,choices=CHOICE,default="")
    women_cloth_name = models.CharField(max_length=100)
    women_cloth_price = models.CharField(max_length=100)
    women_cloth_brand = models.CharField(max_length=100)
    women_cloth_desc = models.TextField()
    women_cloth_image = models.ImageField(upload_to='women_cloths/',default='')
    women_cloth_image1 = models.ImageField(upload_to='women_cloths/',default='plus.png')
    women_cloth_image2 = models.ImageField(upload_to='women_cloths/',default='plus.png')
    women_cloth_image3 = models.ImageField(upload_to='women_cloths/',default='plus.png')
    women_cloth_stock = models.CharField(max_length=100,default='Available')
    women_cloth_proID = models.CharField(max_length=10)
    women_cloth_size = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.username.upper() + " - " + self.women_cloth_name.upper()

# MEN CLOTH MODEL

class MEN_CLOTH(models.Model):
    CHOICE1 = ( 
        ("shirt",'shirt'),
        ("t-shirt",'t-shirt'),
        ("jeans",'jeans'),
        ("jackets",'jackets'),
        ("casual",'casual'),
    )
    men_cloth_category = models.CharField(max_length=100,choices=CHOICE1,default="")
    men_cloth_name = models.CharField(max_length=100)
    men_cloth_price = models.CharField(max_length=100)
    men_cloth_brand = models.CharField(max_length=100)
    men_cloth_desc = models.TextField()
    men_cloth_image = models.ImageField(upload_to='men_cloths/',default='')
    men_cloth_image1 = models.ImageField(upload_to='men_cloths/',default='plus.png')
    men_cloth_image2 = models.ImageField(upload_to='men_cloths/',default='plus.png')
    men_cloth_image3 = models.ImageField(upload_to='men_cloths/',default='plus.png')
    men_cloth_stock = models.CharField(max_length=100,default='Available')
    men_cloth_proID = models.CharField(max_length=10)
    men_cloth_size = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.username.upper() + " - " + self.men_cloth_name.upper()

# WOMEN ACCESSORIES MODEL

class WOMEN_ACCESSORIES(models.Model):
    CHOICE2 = ( 
        ("sunglasses",'sunglasses'),
        ("necklace",'necklace'),
        ("watch",'watch'),
        ("tie",'tie'),
        ("purse",'purse'),
        ("ring",'ring'),
        ("hair_band",'hair_band'),
        ("cap",'cap'),
    )
    women_acc_category = models.CharField(max_length=100,choices=CHOICE2,default="")
    women_acc_name = models.CharField(max_length=100)
    women_acc_price = models.CharField(max_length=100)
    women_acc_brand = models.CharField(max_length=100)
    women_acc_desc = models.TextField()
    women_acc_image = models.ImageField(upload_to='women_acc/',default='')
    women_acc_image1 = models.ImageField(upload_to='women_acc/',default='plus.png')
    women_acc_image2 = models.ImageField(upload_to='women_acc/',default='plus.png')
    women_acc_image3 = models.ImageField(upload_to='women_acc/',default='plus.png')
    women_acc_stock = models.CharField(max_length=100,default='Available')
    women_acc_proID = models.CharField(max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.username.upper() + " - " + self.women_acc_name.upper()

# MEN ACCESSORIES MODEL

class MEN_ACCESSORIES(models.Model):
    CHOICE2 = ( 
        ("m_sunglasses",'m_sunglasses'),
        ("suspenders",'suspenders'),
        ("m_watch",'m_watch'),
        ("m_tie",'m_tie'),
        ("m_purse",'m_purse'),
        ("belt",'belt'),
        ("socks",'socks'),
        ("m_cap",'m_cap'),
    )
    men_acc_category = models.CharField(max_length=100,choices=CHOICE2,default="")
    men_acc_name = models.CharField(max_length=100)
    men_acc_price = models.CharField(max_length=100)
    men_acc_brand = models.CharField(max_length=100)
    men_acc_desc = models.TextField()
    men_acc_image = models.ImageField(upload_to='men_acc/',default='')
    men_acc_image1 = models.ImageField(upload_to='men_acc/',default='plus.png')
    men_acc_image2 = models.ImageField(upload_to='men_acc/',default='plus.png')
    men_acc_image3 = models.ImageField(upload_to='men_acc/',default='plus.png')
    men_acc_stock = models.CharField(max_length=100,default='Available')
    men_acc_proID = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.username.upper() + " - " + self.men_acc_name.upper()

# WOMEN FOOTWEAR MODEL

class WOMEN_FOOTWEAR(models.Model):
    CHOICE2 = ( 
        ("wedges",'wedges'),
        ("ballerinas",'ballerinas'),
        ("canvas_shoes",'canvas_shoes'),
        ("wellington_boots",'wellington_boots'),
        ("flip_flop",'flip_flop'),
        ("sandals",'sandals'),
        ("sport_shoes",'sport_shoes'),
        ("heels",'heels'),
    )
    women_footwear_category = models.CharField(max_length=100,choices=CHOICE2,default="")
    women_footwear_name = models.CharField(max_length=100)
    women_footwear_price = models.CharField(max_length=100)
    women_footwear_brand = models.CharField(max_length=100)
    women_footwear_desc = models.TextField()
    women_footwear_image = models.ImageField(upload_to='women_footwear/',default='')
    women_footwear_image1 = models.ImageField(upload_to='women_footwear/',default='plus.png')
    women_footwear_image2 = models.ImageField(upload_to='women_footwear/',default='plus.png')
    women_footwear_image3 = models.ImageField(upload_to='women_footwear/',default='plus.png')
    women_footwear_stock = models.CharField(max_length=100,default='Available')
    women_footwear_proID = models.CharField(max_length=100)
    women_footwear_size = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.username.upper() + " - " + self.women_footwear_name.upper()

# MEN FOOTWEAR MODEL

class MEN_FOOTWEAR(models.Model):
    CHOICE3 = ( 
        ("m_sandals",'m_sandals'),
        ("m_flipflop",'m_flipflop'),
        ("m_canvas_shoes",'m_canvas_shoes'),
        ("brogues",'brogues'),
        ("oxford",'oxford'),
        ("loafers",'loafers'),
        ("m_sport_shoes",'m_sport_shoes'),
        ("leather",'leather'),
    )
    men_footwear_category = models.CharField(max_length=100,choices=CHOICE3,default="")
    men_footwear_name = models.CharField(max_length=100)
    men_footwear_price = models.CharField(max_length=100)
    men_footwear_brand = models.CharField(max_length=100)
    men_footwear_desc = models.TextField()
    men_footwear_image = models.ImageField(upload_to='men_footwear/',default='')
    men_footwear_image1 = models.ImageField(upload_to='men_footwear/',default='plus.png')
    men_footwear_image2 = models.ImageField(upload_to='men_footwear/',default='plus.png')
    men_footwear_image3 = models.ImageField(upload_to='men_footwear/',default='plus.png')
    men_footwear_stock = models.CharField(max_length=100,default='Available')
    men_footwear_proID = models.CharField(max_length=100,default='')
    men_footwear_size = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.username.upper() + " - " + self.men_footwear_name.upper()

# WISHLIST MODEL

class WISHLIST(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    women_cloth = models.ForeignKey(WOMEN_CLOTH,on_delete=models.CASCADE,null=True)
    women_acc = models.ForeignKey(WOMEN_ACCESSORIES,on_delete=models.CASCADE,null=True)
    women_footwear = models.ForeignKey(WOMEN_FOOTWEAR,on_delete=models.CASCADE,null=True)
    men_cloth = models.ForeignKey(MEN_CLOTH,on_delete=models.CASCADE,null=True)
    men_acc = models.ForeignKey(MEN_ACCESSORIES,on_delete=models.CASCADE,null=True)
    men_footwear = models.ForeignKey(MEN_FOOTWEAR,on_delete=models.CASCADE,null=True)
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username 

# CART MODEL

class CART(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    women_cloth = models.ForeignKey(WOMEN_CLOTH,on_delete=models.CASCADE,null=True)
    women_acc = models.ForeignKey(WOMEN_ACCESSORIES,on_delete=models.CASCADE,null=True)
    women_footwear = models.ForeignKey(WOMEN_FOOTWEAR,on_delete=models.CASCADE,null=True)
    men_cloth = models.ForeignKey(MEN_CLOTH,on_delete=models.CASCADE,null=True)
    men_acc = models.ForeignKey(MEN_ACCESSORIES,on_delete=models.CASCADE,null=True)
    men_footwear = models.ForeignKey(MEN_FOOTWEAR,on_delete=models.CASCADE,null=True)
    added_date = models.DateField(default=timezone.now)
    total_price = models.IntegerField()
    total_qty = models.IntegerField()

    def __str__(self):
        return self.user.username


class CHECKOUT(models.Model):
    COUNTRY = ( 
        ("india",'india'),
    )
    STATE = (
        ("andhra","andhra"),
        ("arunachal","arunachal"),
        ("assam","assam"),
        ("bihar","bihar"),
        ("goa","goa"),
        ("gujrat","gujrat"),
        ("haryana","haryana"),
        ("himachal","himachal"),
        ("jharkhand","jharkhand"),
        ("karnataka","karnataka"),
        ("kerala","kerala"),
        ("mp","mp"),
        ("mh","mh"),
        ("manipur","manipur"),
        ("meghalaya","meghalaya"),
        ("mizoram","mizoram"),
        ("nagaland","nagaland"),
        ("odisha","odisha"),
        ("punjab","punjab"),
        ("rj","rj"),
        ("sikkim","sikkim"),
        ("tn","tn"),
        ("telangana","telangana"),
        ("tripura","tripura"),
        ("up","up"),
        ("uk","uk"),
        ("wb","wb"),
    )
    amount = models.IntegerField(default=0)
    item_size = models.CharField(max_length=5)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    e_mail = models.CharField(max_length=20)
    m_obile = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    add1 = models.CharField(max_length=50)
    add2 = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=20,choices=COUNTRY,default='')
    state = models.CharField(max_length=20,choices=STATE,default='')

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    fname = models.CharField(max_length=20,default='')
    lname = models.CharField(max_length=20,default='')
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)