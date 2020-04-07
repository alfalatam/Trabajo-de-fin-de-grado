# # from .models import Invoice
# from .models import Project
# from django.views.generic import View
# from .models import *
# from .render import Render


# def gen_pdf(request):
#     ids = request.GET.get('id')
#     cid = request.GET.get('cid')
#     sales = Invoice.objects.filter(pk=ids).select_related('projectid')
#     project = Project.objects.filter(pk=cid).select_related('clientname')
#     params = {
#         'sales': sales,
#         'request': request,
#         'project': project
#     }
#     return Render.render('billing/pdf.html', params)

# 0) Create document
# from io import BytesIO
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse


# def pdfGenerator(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

#     buffer = BytesIO()

#     # Create the PDF object, using the BytesIO object as its "file."
#     p = canvas.Canvas(buffer)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")

#     # Close the PDF object cleanly.
#     p.showPage()
#     p.save()

#     # Get the value of the BytesIO buffer and write it to the response.
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#     return response


# import io
# from django.http import FileResponse
# from reportlab.pdfgen import canvas


# def pdfGenerator(request):

#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")

#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()

#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
