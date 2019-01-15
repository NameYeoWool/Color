from PIL import Image #Pillow
from pilkit.processors import Thumbnail


def mkthum(image_source):
    processor = Thumbnail(width=300, height=200)
    mountain_image = Image.open(image_source)

    thumb_image = processor.process(mountain_image)
    thumb_image.save("thumbnail.png",quality=60)