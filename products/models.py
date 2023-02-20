import os
from django.conf import settings
from django.db import models
from datetime import datetime
from PIL import Image


# Path for media save
def upload_path(instance, filename):
    current = datetime.now().date()
    sec = datetime.now().microsecond
    extension = filename.split(".")[-1]
    return f"product/{current}_{sec}.{extension}"


# Create thumbnail from image
def create_thumbnail(input_image, thumbnail_size=(256, 256)):
    # make sure an image has been set
    if not input_image or input_image == "":
        return
    # open image
    image = Image.open(input_image)
    # use PILs thumbnail method; use anti aliasing to make the scaled picture look good
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    # parse the filename and scramble it
    filename = upload_path(None, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    # extension is in the last element, pop it
    extension = arrdata.pop()
    basename = "".join(arrdata)
    # add _thumb to the filename
    new_filename = basename + "_thumb." + extension
    # save the image in MEDIA_ROOT and return the filename
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename))
    return new_filename


# Product Model
class Products(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.title}, {self.qty}, {self.price}"


# Product Images
class Images(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField("Product Image", upload_to=upload_path, blank=True)
    thumb = models.ImageField("Thumbnail", blank=True)

    def __str__(self) -> str:
        return super().__str__()

    # save thumbnail with image
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.thumb = create_thumbnail(self.image)
        return super().save(force_update=force_update)
