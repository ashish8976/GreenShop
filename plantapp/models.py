from django.db import models

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    bio = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=255,null=True)
    pincode = models.IntegerField(null=True)
    landmark = models.CharField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Category(models.Model):
    name       = models.CharField(max_length=100)
    icon       = models.CharField(max_length=10, null=True, blank=True)  
    image      = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = "Category"
        verbose_name_plural = "Categories"    

class Product(models.Model):
    
    # Basic Info
    name            = models.CharField(max_length=200)
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description     = models.TextField()
    care_guide      = models.TextField(null=True, blank=True)
    badge_text      = models.CharField(max_length=50, null=True, blank=True)

    # Plant Details (Specs Tab)
    scientific_name = models.CharField(max_length=200, null=True, blank=True)
    common_name     = models.CharField(max_length=200, null=True, blank=True)
    family          = models.CharField(max_length=100, null=True, blank=True)
    origin          = models.CharField(max_length=200, null=True, blank=True)
    plant_type      = models.CharField(max_length=100, null=True, blank=True)
    mature_height   = models.CharField(max_length=100, null=True, blank=True)
    growth_rate     = models.CharField(max_length=100, null=True, blank=True)
    toxicity        = models.CharField(max_length=200, null=True, blank=True)
    air_purifying   = models.BooleanField(default=False)

    # Care Info
    watering        = models.CharField(max_length=100, null=True, blank=True)
    sunlight        = models.CharField(max_length=100, null=True, blank=True)
    temperature     = models.CharField(max_length=100, null=True, blank=True)
    humidity        = models.CharField(max_length=100, null=True, blank=True)

    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = "Product"
        verbose_name_plural = "Products"


class ProductSize(models.Model):

    product        = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size_name      = models.CharField(max_length=50)
    pot_size_label = models.CharField(max_length=100, null=True, blank=True)
    order          = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.size_name}"

    class Meta:
        verbose_name        = "Product Size"
        verbose_name_plural = "Product Sizes"
        ordering            = ['order']


class ProductPot(models.Model):

    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pots')
    pot_name = models.CharField(max_length=100)
    icon     = models.CharField(max_length=10)
    order    = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.pot_name}"

    class Meta:
        verbose_name        = "Product Pot"
        verbose_name_plural = "Product Pots"
        ordering            = ['order']


class ProductVariant(models.Model):

    size      = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='variants')
    pot       = models.ForeignKey(ProductPot,  on_delete=models.CASCADE, related_name='variants')
    price     = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock     = models.IntegerField(default=0)
    sku       = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def is_available(self):
        return self.stock > 0

    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((self.old_price - self.price) / self.old_price * 100)
        return 0

    def __str__(self):
        return f"{self.size} + {self.pot.pot_name} → ₹{self.price}"

    class Meta:
        verbose_name        = "Product Variant"
        verbose_name_plural = "Product Variants"
        unique_together     = ('size', 'pot')


class ProductImage(models.Model):

    size  = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.size} - Image {self.order}"

    class Meta:
        verbose_name        = "Product Image"
        verbose_name_plural = "Product Images"
        ordering            = ['order']



class Review(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    rating    = models.IntegerField(default=5)  # 1 to 5
    comment   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} - {self.rating}★"

    class Meta:
        verbose_name        = "Review"
        verbose_name_plural = "Reviews"
        
class Wishlist(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} → {self.product.name}"


class cart(models.Model):
    pass

class order(models.Model):
    pass

class payment(models.Model):
    pass

