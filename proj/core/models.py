from django.db import models
from django.contrib.auth.models import Group, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have an email address!')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,**extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,name,password, **extra_fields):
        user = self.create_user(email,name,password,**extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    class Role(models.TextChoices):
        SELLER = "SELLER",'Seller'
        CUSTOMER = "CUSTOMER",'Customer'

    base_role=Role.SELLER
    role=models.CharField(max_length=255,choices=Role.choices)    
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    phone_number=models.CharField(validators=[],max_length=20)
    phone_regex= RegexValidator(
        regex=r'^0(6|7|5|3)\d{8}$',
        message="phone number should start with 06 07 05 or 03"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','last_name','address','phone_number']
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects=CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.Role = self.base_role
        super().save(*args, **kwargs)
        group_name = self.role  # Group name should match the role name in lowercase
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)

    def __str__(self):
        return self.email    

class Category(models.Model):
    name=models.CharField(max_length=255,unique=True)
    description=models.CharField(default='',max_length=255) 

    def __str__(self):
        return self.name     

class Product(models.Model):
    name = models.CharField(max_length=255,unique=True)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    price = models.CharField(max_length=50)
    image = models.ImageField(default='', upload_to='images/') 
    category_prod = models.ForeignKey(
        Category,
        to_field='name',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    order_by = models.ForeignKey(
        User,
        editable=False,
        on_delete=models.CASCADE
    )
    product=models.ForeignKey(
        Product,
        to_field='name',
        on_delete=models.CASCADE
    )
