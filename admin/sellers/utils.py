import os, secrets
from flask_mail import Message
from admin import mail, app


def save_document(image_files):
    for image_file in image_files:
        random_hax = secrets.token_hex(8)
        _,f_ext = os.path.splitext(image_file.filename)
        image_filename = random_hax+f_ext
        image_path = os.path.join(app.root_path,'static/document',image_filename)
        # img_size = (400,400)
        # img = Image.open(image_file)
        # img.thumbnail(img_size)
        image_file.save(image_path)
    return image_filename

def send_otp_mail(data):
    msg = Message("Email Verification",sender="noreply@demo.com",recipients=[data['email']])
    msg.body = f"""Verify your mail
OTP is {data['otp']}
if its no you leave it... """
    mail.send(msg)