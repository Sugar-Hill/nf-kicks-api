from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug is not instance.title:
        instance.slug = slugify(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)


def product_image_upload_to(instance, filename):
    title = instance.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "products/%s/%s" % (slug, new_filename)


def product_images_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "products/%s/%s" % (slug, new_filename)


class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField()
    categories = models.ManyToManyField(Category, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_upload_to)

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug is not instance.title:
        instance.slug = slugify(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_images_upload_to)

    def __str__(self):
        return self.product.title


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = (
            ('product', 'name')
        )

    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=10)
    # TODO: Decrease the stock when a purchase is made
    stock = models.IntegerField()

    class Meta:
        unique_together = (
            ('variation', 'value')
        )

    def __str__(self):
        return self.value
