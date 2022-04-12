import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import ListView
from num2words import num2words
from xhtml2pdf import pisa

from api.models import Report


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path



def render_pdf_view(last_transaction_id):
    cur_policy = Report.objects.get(transaction_id=last_transaction_id)
    # template_path = 'pdf/customer_template.html' # local
    template_path = 'pdf/prod_template.html'  # Docker
    context = {
        "client_name" : cur_policy.client_name,
        "client_address" : cur_policy.client_address,
        "client_phone" : cur_policy.client_phone,
        "client_passport" : cur_policy.client_passport,
        "insurance_cost": int(cur_policy.insurance_cost),
        "insurance_cost_word": num2words(int(cur_policy.insurance_cost), lang='ru'),

        "insurance_premium" : int(cur_policy.insurance_premium),
        "insurance_premium_word": num2words(int(cur_policy.insurance_premium), lang='ru'),

        "insurance_liability" : int(cur_policy.insurance_liability),
        "insurance_liability_word": num2words(int(cur_policy.insurance_liability), lang='ru'),

        "polis_sery": cur_policy.polis_sery,
        "polis_number": cur_policy.polis_number,
        "polis_begin": datetime.strftime(cur_policy.polis_begin, '%d.%m.%Y'),
        "polis_end": datetime.strftime(cur_policy.polis_end, '%d.%m.%Y'),
        "uuid": cur_policy.uuid,
        "qrcode": cur_policy.qrcode
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if only displayed
    filename = f'media/pdf/{last_transaction_id}.pdf'
    print(filename)

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    file = open(filename, "wb")

    pisa_status = pisa.CreatePDF(
        html.encode('utf-8'),
        dest=file,
        encoding='utf-8'
    )
    file.close()

    # if error then show some funy view

    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # print(link_callback)
    return filename

def prod_template(request):
    return render(request, 'pdf/prod_template.html')