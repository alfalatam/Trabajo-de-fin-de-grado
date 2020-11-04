from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from django import forms
from recibo.models import Ticket, TicketLink
from producto.models import Producto
from Proyecto.settings import STATIC_URL, MEDIA_URL
from datetime import datetime
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Image
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from recibo.views import importeTotal
from django.shortcuts import redirect
from django.shortcuts import render
import json
import textwrap


def generate_pdf(request, *args, **kwargs):

    if request.method == 'GET':

        reciboID = request.GET.get('recibo')
        recibos = Ticket.objects.all()
        recibo = recibos.get(pk=reciboID)

        # TODO
        # productosRecibo = Producto.objects.filter(ticket=recibo)
        productosRecibo = Producto.objects.all()

        data = recibo.data

        if (recibo.data is not None):
            try:
                # a_json = json.loads(a_string)
                jsonData = json.loads(data)
                print(jsonData)

                if (jsonData is dict):
                    jsonData = None

            except ValueError as e:
                print(e)
                if (data):
                    data = ""
                # jsonData = json.loads(data)
                # print('=======2=========')
                # print(jsonData)

        response = HttpResponse(content_type='application/pdf')
        # pdf_name = "clientes.pdf"  # llamado clientes
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (
            recibo.title,)
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=60,
                            bottomMargin=50,
                            )

    negrita = ParagraphStyle('parrafos',

                             fontSize=12,
                             fontName="Times-bold")

    tabla1 = ParagraphStyle('tablas',

                            fontSize=12,
                            fontName="Times-bold")

    clientes = []
    styles = getSampleStyleSheet()
    # header = Paragraph("Listado de Clientes", styles['Heading1'])
    # clientes.append(header)
    # solicitado = Paragraph(
    #     u"SOLICITADO POR: " + requerimiento.solicitante.nombre_completo(), izquierda)

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
                '/companyLogo/%s.png' % (recibo.companyIdentifier)
            # image2 = MEDIA_URL + '/companyLogo/base.png'
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

    # Aqui esta la chicha jsonData
    # jsonData

    if (data):
        # print('=====================================')
        # print(jsonData)
        # print(type(jsonData))

        productos = [(textwrap.fill(p["name"], 40), p["quantity"], p["price"]+' €', p["priceIVA"]+' €', str((float(p["priceIVA"])*int(p["quantity"])))+' €')
                     for p in jsonData]

        # elif (jsonData is dict):
        #     print('9999999999999999999999999')
        #     listA = []
        #     listA.append(jsonData)
        #     productos = [(textwrap.fill(p["name"], 40), p["quantity"], p["price"]+' €', p["priceIVA"]+' €', str((float(p["priceIVA"])*int(p["quantity"])))+' €')
        #                  for p in listA]
        # else:
        #     productos = []

        # productos=[]

    # productos = [(p.name, p.quantity, p.price, p.price*p.quantity)
    #              for p in productosRecibo]

    if (data):
        t = Table([headings] + productos, spaceAfter=200, spaceBefore=800)
    else:
        t = Table([headings], spaceAfter=200,  spaceBefore=800)

    # t.setStyle(TableStyle(
    #     [
    #         ('LINEABOVE', (1, 2), (-2, 2), 5, colors.blue),
    #         ('ALIGN', (100, 100), (100, -1), 'RIGHT'),
    #         ('GRID', (0, 0), (3, -1), 1, colors.black),
    #         ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.white),

    #     ]
    # ))

    # t.levelStyles = [
    #     spaceBefore = 10,

    # ]
    # clientes.append(t)
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

    # hAlign = TA_LEFT
    t2 = Table([empty],  spaceAfter=300)
    # cmds = t.se.getCommands()
    # print(cmds)
    clientes.append(t2)
    clientes.append(t)

    # -----------------------------------------------------------------------------------
    t.spaceBefore = 20
    doc.build(clientes, onFirstPage=pageSetup, onLaterPages=pageSetup2)
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
                # a_json = json.loads(a_string)
                jsonData = json.loads(data)
                print(jsonData)

                if (jsonData is dict):
                    jsonData = None

            except ValueError as e:
                if (data):
                    data = ""
                # jsonData = json.loads(data)
                # print('=======2=========')
                # print(jsonData)

        print(ticketLink.is_shared)
        response = HttpResponse(content_type='application/pdf')
        # pdf_name = "clientes.pdf"  # llamado clientes
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (
            recibo.title)
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=60,
                            bottomMargin=50,
                            )

    negrita = ParagraphStyle('parrafos',

                             fontSize=12,
                             fontName="Times-bold")

    tabla1 = ParagraphStyle('tablas',

                            fontSize=12,
                            fontName="Times-bold")

    clientes = []
    styles = getSampleStyleSheet()
    # header = Paragraph("Listado de Clientes", styles['Heading1'])
    # clientes.append(header)
    # solicitado = Paragraph(
    #     u"SOLICITADO POR: " + requerimiento.solicitante.nombre_completo(), izquierda)

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
                '/companyLogo/%s.png' % (recibo.companyIdentifier)
            # image2 = MEDIA_URL + '/companyLogo/base.png'
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

    # Aqui esta la chicha jsonData
    # jsonData
    if (data):
        # print('=====================================')
        # print(jsonData)
        # print(type(jsonData))

        productos = [(textwrap.fill(p["name"], 40), p["quantity"], p["price"]+' €', p["priceIVA"]+' €', str((float(p["priceIVA"])*int(p["quantity"])))+' €')
                     for p in jsonData]
        # elif (jsonData is dict):
        #     print('9999999999999999999999999')
        #     listA = []
        #     listA.append(jsonData)
        #     productos = [(textwrap.fill(p["name"], 40), p["quantity"], p["price"]+' €', p["priceIVA"]+' €', str((float(p["priceIVA"])*int(p["quantity"])))+' €')
        #                  for p in listA]
        # else:
        #     productos = []

        # productos=[]

    # productos = [(p.name, p.quantity, p.price, p.price*p.quantity)
    #              for p in productosRecibo]

    if (data):
        t = Table([headings] + productos, spaceAfter=200, spaceBefore=800)
    else:
        t = Table([headings], spaceAfter=200,  spaceBefore=800)

    # t.setStyle(TableStyle(
    #     [
    #         ('LINEABOVE', (1, 2), (-2, 2), 5, colors.blue),
    #         ('ALIGN', (100, 100), (100, -1), 'RIGHT'),
    #         ('GRID', (0, 0), (3, -1), 1, colors.black),
    #         ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.white),

    #     ]
    # ))

    # t.levelStyles = [
    #     spaceBefore = 10,

    # ]
    # clientes.append(t)
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

    # hAlign = TA_LEFT
    t2 = Table([empty],  spaceAfter=300)
    # cmds = t.se.getCommands()
    # print(cmds)
    clientes.append(t2)
    clientes.append(t)

    # -----------------------------------------------------------------------------------
    t.spaceBefore = 20
    doc.build(clientes, onFirstPage=pageSetup, onLaterPages=pageSetup2)
    response.write(buff.getvalue())
    buff.close()
    return response

    # return render(request, 'inicio.html', context=None, content_type=None, status=None, using=None)
