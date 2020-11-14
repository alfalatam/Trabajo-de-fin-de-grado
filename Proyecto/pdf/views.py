from io import BytesIO
# from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
# from django import forms
from recibo.models import Ticket, TicketLink
# from producto.models import Producto
from Proyecto.settings import MEDIA_URL
from datetime import datetime
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
# from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
# from reportlab.lib.units import inch
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from recibo.views import importeTotal
# from django.shortcuts import redirect
# from django.shortcuts import render
import json
import textwrap


def generate_pdf(request, *args, **kwargs):

    if request.method == 'GET':

        # Obtenemos la información del recibo
        reciboID = request.GET.get('recibo')
        recibos = Ticket.objects.all()
        recibo = recibos.get(pk=reciboID)
        # Data del recibo de compra que contiene la información del producto
        data = recibo.data

        if (recibo.data is not None):
            try:
                # convertimos el tipo a un json
                jsonData = json.loads(data)

                if (jsonData is dict):
                    jsonData = None

            # Si da algún error la conversión igualamos el data a una cadena vacía
            except ValueError as e:
                print(e)
                if (data):
                    data = ""

        # Indicador de que el objeto a cargar debe ser un pdf
        response = HttpResponse(content_type='application/pdf')
        # Este indicador de que se debe mostrar con un download se descargaría directamente
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (
            recibo.title,)

    buff = BytesIO()
    # Datos básicos del formato de las páginas del PDF
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=60,
                            bottomMargin=50,
                            )

    listC = []

    # -------------------------Marca de agua ---------------------------------------------

    def pageSetup(canvas, doc):

        canvas.saveState()

        # Marca de agua de la página
        image2 = MEDIA_URL + \
            '/watermark.png'
        canvas.saveState()
        canvas.rotate(10)
        canvas.drawImage(image2, 200, 280, width=320, height=110, mask='auto')

        canvas.restoreState()
        # Fuente a utilizar en el documento
        registerFont(TTFont('Calibri', 'Calibri.ttf'))

        # Imagen de la compañia

        try:
            image2 = MEDIA_URL + \
                '/companyLogo/%s' % (recibo.companyIdentifier)
            canvas.drawImage(image2, 350, 700, width=200,
                             height=90, mask='auto')
        # Si no tiene imagen o hay algún error con su imagen carga una genérica
        except OSError:
            image2 = MEDIA_URL + '/companyLogo/base.png'
            canvas.drawImage(image2, 350, 700, width=200,
                             height=90, mask='auto')

    # Fecha
        canvas.setFont('Times-Bold', 11)
        canvas.drawString(75, 750, 'Fecha: ')
        canvas.setFont("Calibri", 11)
        canvas.drawString(110, 750, datetime.today().strftime('%d/%m/%Y'))

    # Nombre

        # canvas.setFont('Times-Bold', 11)
        # canvas.drawString(75, 725, 'Cliente: ')
        # canvas.setFont("Calibri", 11)
        # canvas.drawString(
        #     115, 725, recibo.user.first_name + " " + recibo.user.last_name)

    # Titulo del recibo
        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 625, 'Título del recibo:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(158, 625, recibo.title)

    # Empresa

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 600, 'Empresa:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(123, 600, recibo.empresa)

    # Dirección

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 575, 'Dirección:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(125, 575, recibo.address)

    # Importe

        ipt = importeTotal(recibo)
        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 550, 'Importe total:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(144, 550, str(ipt)+' €')

    # Método de pago
        metodoDePago = ''

        if(recibo.payment == 'TD'):
            metodoDePago = 'Tarjeta de débito'
        elif(recibo.payment == 'TC'):
            metodoDePago = 'Tarjeta de crédito'
        else:
            metodoDePago = 'Efectivo'

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 525, 'Método de pago: ')
        canvas.setFont("Calibri", 11)
        canvas.drawString(156, 525, metodoDePago)

    # Identificador único

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 500, 'Identificador(ID): ')
        canvas.setFont("Calibri", 11)
        canvas.drawString(162, 500, recibo.identifier)

    # -----------------------------------------------------------------------
    # Formato para las páginas despues de la primera
    def pageSetup2(canvas, doc):

        canvas.saveState()
        # Marca de agua
        image2 = MEDIA_URL + \
            '/watermark.png'
        canvas.saveState()
        canvas.rotate(10)
        canvas.drawImage(image2, 200, 280, width=320, height=110, mask='auto')

        canvas.restoreState()
        # Fuente
        registerFont(TTFont('Calibri', 'Calibri.ttf'))

    # ---------------------- Tabla de productos -------------------------------------------
    headings = ('Nombre', 'Cantidad', 'precio sin IVA', 'precio con IVA',
                'Precio total(IVA incluido)')

    empty = ('')

    # Recorremos el listado de productos y los guardamos para cargarlos en la tabla
    if (data):

        productos = [(textwrap.fill(p["name"], 40), p["quantity"], p["price"]+' €', p["priceIVA"]+' €', str((float(p["priceIVA"])*int(p["quantity"])))+' €')
                     for p in jsonData]

    if (data):
        t = Table([headings] + productos, spaceAfter=200, spaceBefore=800)
    else:
        t = Table([headings], spaceAfter=200,  spaceBefore=800)

    # Estilo
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('TEXTCOLOR', (0, 0), (3, 0), colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                           ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('ROWHEIGHT', (0, 0), (-1, -1), 20),
                           ('TOPPADDING', (0, 0), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6),


                           ]))

    t2 = Table([empty],  spaceAfter=300)
    listC.append(t2)
    listC.append(t)

    # -----------------------------------------------------------------------------------
    t.spaceBefore = 20
    # Definimos el formato para cada página
    doc.build(listC, onFirstPage=pageSetup, onLaterPages=pageSetup2)
    response.write(buff.getvalue())
    buff.close()
    return response


def generate_public_pdf(request, *args, **kwargs):

    if request.method == 'GET':

        reciboID = request.GET.get('url')
        ticketLink = TicketLink.objects.get(url=reciboID)
        recibo = ticketLink.ticket

        data = recibo.data
        if (recibo.data is not None):
            try:
                jsonData = json.loads(data)

                if (jsonData is dict):
                    jsonData = None

            except ValueError as e:
                if (data):
                    data = ""

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (
            recibo.title)

    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=60,
                            bottomMargin=50,
                            )

    listC = []
    # -------------------------Marca de agua ---------------------------------------------
    def pageSetup(canvas, doc):

        canvas.saveState()

        image2 = MEDIA_URL + \
            '/watermark.png'
        canvas.saveState()
        canvas.rotate(10)
        canvas.drawImage(image2, 200, 280, width=320, height=110, mask='auto')

        canvas.restoreState()
        registerFont(TTFont('Calibri', 'Calibri.ttf'))

        # Imagen de la compañia
        try:
            image2 = MEDIA_URL + \
                '/companyLogo/%s' % (recibo.companyIdentifier)
            canvas.drawImage(image2, 350, 700, width=200,
                             height=90, mask='auto')

        except OSError:
            image2 = MEDIA_URL + '/companyLogo/base.png'
            canvas.drawImage(image2, 350, 700, width=200,
                             height=90, mask='auto')

    # Fecha
        canvas.setFont('Times-Bold', 11)
        canvas.drawString(75, 750, 'Fecha: ')
        canvas.setFont("Calibri", 11)
        canvas.drawString(110, 750, datetime.today().strftime('%d/%m/%Y'))

    # Nombre

        # canvas.setFont('Times-Bold', 11)
        # canvas.drawString(75, 725, 'Cliente: ')
        # canvas.setFont("Calibri", 11)
        # canvas.drawString(
        #     115, 725, recibo.user.first_name + " " + recibo.user.last_name)

    # Titulo del recibo
        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 625, 'Título del recibo:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(158, 625, recibo.title)

    # Empresa

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 600, 'Empresa:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(123, 600, recibo.empresa)

    # Dirección

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 575, 'Dirección:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(125, 575, recibo.address)

    # Importe

        ipt = importeTotal(recibo)
        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 550, 'Importe total:')
        canvas.setFont("Calibri", 11)
        canvas.drawString(144, 550, str(ipt)+' €')

    # Método de pago
        metodoDePago = ''

        if(recibo.payment == 'TD'):
            metodoDePago = 'Tarjeta de débito'
        elif(recibo.payment == 'TC'):
            metodoDePago = 'Tarjeta de crédito'
        else:
            metodoDePago = 'Efectivo'

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 525, 'Método de pago: ')
        canvas.setFont("Calibri", 11)
        canvas.drawString(156, 525, metodoDePago)

    # Identificador único

        canvas.setFont("Times-Bold", 11)
        canvas.drawString(75, 500, 'Identificador(ID): ')
        canvas.setFont("Calibri", 11)
        canvas.drawString(162, 500, recibo.identifier)

    #         p.restoreState()

    # -----------------------------------------------------------------------
    def pageSetup2(canvas, doc):

        canvas.saveState()

        image2 = MEDIA_URL + \
            '/watermark.png'
        canvas.saveState()
        canvas.rotate(10)
        canvas.drawImage(image2, 200, 280, width=320, height=110, mask='auto')

        canvas.restoreState()
        registerFont(TTFont('Calibri', 'Calibri.ttf'))

        # ---------------------- Tabla de productos -------------------------------------------
    headings = ('Nombre', 'Cantidad', 'precio sin IVA', 'precio con IVA',
                'Precio total(IVA incluido)')

    empty = ('')

    if (data):

        productos = [(textwrap.fill(p["name"], 40), p["quantity"], p["price"]+' €', p["priceIVA"]+' €', str((float(p["priceIVA"])*int(p["quantity"])))+' €')
                     for p in jsonData]

    if (data):
        t = Table([headings] + productos, spaceAfter=200, spaceBefore=800)
    else:
        t = Table([headings], spaceAfter=200,  spaceBefore=800)

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('TEXTCOLOR', (0, 0), (3, 0), colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                           ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('ROWHEIGHT', (0, 0), (-1, -1), 20),
                           ('TOPPADDING', (0, 0), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6),


                           ]))

    t2 = Table([empty],  spaceAfter=300)
    # cmds = t.se.getCommands()
    # print(cmds)
    listC.append(t2)
    listC.append(t)
    # -----------------------------------------------------------------------------------
    t.spaceBefore = 20
    doc.build(clientes, onFirstPage=pageSetup, onLaterPages=pageSetup2)
    response.write(buff.getvalue())
    buff.close()
    return response
