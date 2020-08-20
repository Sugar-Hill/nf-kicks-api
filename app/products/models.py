import uuid

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.validators import (
    validate_slug,
    validate_image_file_extension,
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator
)
from django.core.exceptions import ValidationError


def validate_image_size(file):
    filesize = file.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True, validators=[
                             MinLengthValidator(1), MaxLengthValidator(120)])
    slug = models.SlugField(unique=True, blank=True,
                            editable=False, validators=[validate_slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


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


# TODO: Delete this
def product_images_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "products/%s/%s" % (slug, new_filename)


class Product(models.Model):
    title = models.CharField(
        max_length=120,
        unique=True,
        blank=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(120)]
    )
    price = models.FloatField(
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(10000)])
    categories = models.ManyToManyField(Category, blank=True)
    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
        validators=[validate_slug]
    )
    description = models.TextField(blank=False)
    image = models.ImageField(
        upload_to=product_image_upload_to,
        blank=False,
        validators=[validate_image_file_extension, validate_image_size]
    )
    # TODO Drop the DB to use this
    # nfc_code = models.CharField(max_length=100, editable=False, unique=True)

    def __str__(self):
        return self.title


def product_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug is not instance.title:
        instance.slug = slugify(instance)


# def product_nfc_code_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.nfc_code:
#         instance.nfc_code = str(uuid.uuid4())


pre_save.connect(product_slug_pre_save_receiver, sender=Product)

# pre_save.connect(product_nfc_code_pre_save_receiver, sender=Product)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        blank=False,
        upload_to=product_images_upload_to,
        validators=[validate_image_file_extension, validate_image_size]
    )

    def __str__(self):
        return f"Images for {self.product.title}"


SIZE_CHOICES = (
    (3.0, 3.0),
    (4.0, 4.0),
    (6.0, 6.0),
    (6.5, 6.5),
    (7.0, 7.0),
    (7.5, 7.5),
    (8.0, 8.0),
    (8.5, 8.5),
    (9.0, 9.0),
    (9.5, 9.5),
    (10.0, 10.0),
    (10.5, 10.5),
    (11.0, 11.0),
    (11.5, 11.5),
    (12.0, 12.0),
    (12.5, 12.5),
    (13.0, 13.0),
)


class Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.FloatField(choices=SIZE_CHOICES, blank=False, validators=[
        MinValueValidator(0), MaxValueValidator(10000)])
    # TODO: Decrease the stock when a purchase is made
    stock = models.PositiveIntegerField(default=100, validators=[
        MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.product.title}, size {self.size}"
