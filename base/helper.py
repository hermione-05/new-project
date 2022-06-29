from io import BytesIO
from re import template
from urllib import response
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf.pisa import pisaDocument
import uuid

def save_pdf(param:dict):
    template = get_template("invoice_mail.html")
    html = template.render(param)

    response = BytesIO()
    pdf = pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name = uuid.uuid4()

    try:
        with open(str(settings.BASE_DIR)+f"/media/pdfs/{file_name}.pdf","wb+") as output:
            pdf = pisaDocument(BytesIO(html.encode('UTF-8')),output)

    except Exception as e:
        print(e)

    if pdf.err:
        return '',False
    else:
        return file_name,True

