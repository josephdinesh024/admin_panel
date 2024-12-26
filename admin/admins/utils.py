import os, secrets, io
from PIL import Image
from  admin import app
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

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


def create_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    sellers = data.get('seller')
    products = data.get('product')
    if sellers:
        print(height)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 50, f"Seller Report")
        c.setFont("Helvetica", 10)
    # Create table data (header + rows)
        table_data = [['Seller Name', 'Company Name', 'Email Id', 'Mobile Number','Products', 'Created Date']]
        for order in sellers:
            table_data.append([order.seller_name, order.company_name, order.email_id, order.mobile_number, len(order.product) ,order.created_date.strftime('%Y-%m-%d')])
    
        # Create a table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        table_width, table_height = table.wrapOn(c, width, height)
        if table_height > height - 100:  # Assuming space needed for header
            c.showPage()
            table.drawOn(c, x=50, y=height - table_height - 50)
        else:
            table.drawOn(c, x=50, y=height - table_height - 100)

        height = height-table_height - 100
        print('seller',height)

    if products:
        print(height)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 50, f"Product Report")
        c.setFont("Helvetica", 10)
    # Create table data (header + rows)
        table_data = [['Seller Name', 'Company Name', 'Product Name', 'Product Quantity','Price', 'Created Date', 'Updated Date']]
        for order in products:
            table_data.append([order.seller.seller_name, order.seller.company_name, order.product_name, order.product_quantity, order.product_price ,order.created_date.strftime('%Y-%m-%d'),order.updated_date.strftime('%Y-%m-%d')])
    
        # Create a table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        table_width, table_height = table.wrapOn(c, width, height)
        if table_height > height - 100:  # Assuming space needed for header
            c.showPage()
            table.drawOn(c, x=50, y=height - table_height - 50)
        else:
            table.drawOn(c, x=50, y=height - table_height - 100)

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')