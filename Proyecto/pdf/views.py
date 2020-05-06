from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from django import forms
from recibo.models import Ticket
from Proyecto.settings import STATIC_URL, MEDIA_URL
from datetime import datetime
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(request):

    # ------------------------Aquí compruebo el get del template -------------------------------------

    if request.method == 'GET':
        reciboID = request.GET.get('recibo')
        recibos = Ticket.objects.filter(user=request.user)
        recibo = recibos.get(pk=reciboID)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (
            recibo.title,)

    # -------------------------Aquí especifico el formato del pdf --------------------------------------

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4, initialFontSize=14)

        registerFont(TTFont('Calibri', 'Calibri.ttf'))
        p.setFont("Calibri", 11)
        p.setFont('Times-Bold', 11)

        p.setLineWidth(600)
        # Just some font imports

    # --------------------- Start writing the PDF here--------------------------------------------

    # Marca de agua
        image2 = MEDIA_URL + \
            '/watermark.png'
        p.saveState()
        p.rotate(10)
        p.drawImage(image2, 200, 300, width=320, height=110, mask='auto')

        p.restoreState()
    # Fecha
        p.setFont('Times-Bold', 11)
        p.drawString(75, 750, 'Fecha: ')
        p.setFont("Calibri", 11)
        p.drawString(110, 750, datetime.today().strftime('%d/%m/%Y'))

    # Nombre

        p.setFont('Times-Bold', 11)
        p.drawString(75, 725, 'Cliente: ')
        p.setFont("Calibri", 11)
        p.drawString(115, 725, recibo.user.username)

    # Imagen de la compañia
        try:
            image2 = MEDIA_URL + \
                '/companyLogo/%s.png' % (recibo.companyIdentifier)
            p.drawImage(image2, 350, 700, width=200, height=100, mask='auto')

        except OSError:
            image2 = MEDIA_URL + '/companyLogo/base.png'
            p.drawImage(image2, 350, 700, width=200, height=100, mask='auto')

    # Titulo del recibo
        p.setFont("Times-Bold", 11)
        p.drawString(75, 625, 'Título del recibo:')
        p.setFont("Calibri", 11)
        p.drawString(158, 625, recibo.title)

    # Empresa

        p.setFont("Times-Bold", 11)
        p.drawString(75, 600, 'Empresa:')
        p.setFont("Calibri", 11)
        p.drawString(123, 600, recibo.empresa)

    # Importe
        p.setFont("Times-Bold", 11)
        p.drawString(75, 575, 'Importe total:')
        p.setFont("Calibri", 11)
        p.drawString(144, 575, str(recibo.price)+' €')

    # Método de pago
        metodoDePago = ''

        if(recibo.payment == 'TD'):
            metodoDePago = 'Tarjeta de débito'
        elif(recibo.payment == 'TC'):
            metodoDePago = 'Tarjeta de crédito'
        else:
            metodoDePago = 'Efectivo'

        p.setFont("Times-Bold", 11)
        p.drawString(75, 550, 'Método de pago: ')
        p.setFont("Calibri", 11)
        p.drawString(156, 550, metodoDePago)

    # Identificador único

        p.setFont("Times-Bold", 11)
        p.drawString(75, 525, 'Identificador(ID): ')
        p.setFont("Calibri", 11)
        p.drawString(162, 525, recibo.identifier)

    # La tabla de productos

        # data = [[1, 2, 3], [2, 1, 3], [3, 2, 1]]

        # table = Table(data, colWidths=10*mm)
        # table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        #                 ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        #                 ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)])

        # table.wrapOn(p, 200, 250)
        # table.drawOn(p, 0*mm, 5*mm)

        # styles = getSampleStyleSheet()
        # ptext = "This is an example."
        # pd = Paragraph(ptext, style=styles["Normal"])
        # pd.drawOn(p, 0*mm, 0*mm)    # position of text / where to draw

        data = [['00', '01', '02', '03', '04'],
                ['10', '11', '12', '13', '14'],
                ['20', '21', '22', '23', '24'],
                ['30', '31', '32', '33', '34']]

        table = Table(data, colWidths=10*mm)

        table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)])

        table.draw

        # p.save()
    # -------------------------------End writing--------------------------------------------

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
