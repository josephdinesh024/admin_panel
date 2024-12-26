import os, secrets
from PIL import Image
from  admin import app

def save_product(image_file):
    random_hax = secrets.token_hex(8)
    _,f_ext = os.path.splitext(image_file.filename)
    image_filename = random_hax+f_ext
    image_path = os.path.join(app.root_path,'static/products',image_filename)
    img_size = (400,400)
    img = Image.open(image_file)
    img.thumbnail(img_size)
    img.save(image_path)
    return image_filename
