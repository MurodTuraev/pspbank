import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from rest_framework import status
from django.db import transaction

from rest_framework.response import Response
from rest_framework.views import APIView

from psb import settings
from .models import Initiate, Perform, Termination, Report
from .serializers import InitiateSerializer, PerformSerializer, TerminationSerializer, ReportSerializer

import qrcode
from pdf.views import render_pdf_view




def index(request):
    return render(request, 'psb/policy.html')


class InitiateTransactionAPIView(APIView):

    def get(self, request):
        initiate = Initiate.objects.all()
        serializer = InitiateSerializer(initiate, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = InitiateSerializer(data=request.data)
        query = Initiate.objects.filter(transaction_id=request.data['transaction_id'])
        if serializer.is_valid() and not query:  # transaction_id бор йуклиги текшириляпти
            insurance_premium = ( float(request.data['insurance_cost']) * 3.9 ) / 100
            insurance_liability = float(request.data['insurance_cost']) * 1.3
            data = {
                "result": 0,
                "result_message": "Успешная обработка запроса. Заявления принята",
                "insurance_premium": insurance_premium,
                "insurance_liability": insurance_liability
            }
            serializer.save()
            initiate_report(serializer, data=data, transaction_id=request.data['transaction_id']) # Report tablega malumot yozish
        else:
            result_message = f"Транзакция {request.data['transaction_id']} - уже существует в базе данных."
            data = {
                "result": 2,
                "result_message": result_message
            }
        # return Response(data=serializer.errors)
        return Response(data=data)



class PerformTransactionAPIView(APIView):

    def get(self, request):
        perform = Perform.objects.all()
        serializer = PerformSerializer(perform, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = PerformSerializer(data=request.data)
        query = Perform.objects.filter(transaction_id=request.data['transaction_id'])
        if serializer.is_valid() and not query:  # transaction_id бор йуклиги текшириляпти
            serializer.save()

            # # QR-CODE
            last_transaction = Report.objects.values('transaction_id').last()
            last_transaction_id = last_transaction['transaction_id']
            file_url = settings.GLOBAL_URL + '/media/pdf/' + str(last_transaction_id) + '.pdf' # pdf faylga ssilka
            qr_name = str(last_transaction_id)
            qr_url = gen_qrcode(url=file_url)
            qr_url.save('media/qrcode/' + qr_name + '.png', 'png')
            qrcode = os.path.relpath(qr_name + '.png')
            qrcode_url = settings.GLOBAL_URL + '/media/qrcode/'+qrcode


            data = {
                "result": 0,
                "result_message": "Успешная обработка запроса. Полис создан",
                "polis_sery": "INSUZ",
                "polis_number": serializer.data['id'],
                "polis_begin": request.data['payment_date'],
                "polis_end": get_polis_end(request.data['payment_date']),
                "qrcode_url": qrcode_url,
                "pdf": file_url
            }
            perform_report(serializer, data=data, transaction_id=request.data['transaction_id'])  # Report tablega malumot yozish

            # PDF generate
            pdf = render_pdf_view(last_transaction_id)

        else:
            result_message = "Ошибка в дате поступление"
            data = {
                "result": 6,
                "result_message": result_message
            }

        # return Response(data=serializer.errors)
        return Response(data=data)



class TerminationTransactionAPIView(APIView):

    def get(self, request):
        termination = Termination.objects.all()
        serializer = TerminationSerializer(termination, many=True)
        return Response(data=serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = TerminationSerializer(data=request.data)
        query = Report.objects.filter(polis_number=request.data['polis_number']) # Report tabledan tekshirish kerak
        if serializer.is_valid() and query:  # transactionda polis_number бор йуклиги текшириляпти
            data = {
                "result": 0,
                "result_message": "Успешная обработка запроса. Расторжение выполнено",
                "term_amount": 13
            }
            serializer.save()
            termination_report(serializer, data, request.data['polis_number'])
        else:
            result_message = "Полис не найден"
            data = {
                "result": 1,
                "result_message": result_message
            }

        # return Response(data=serializer.errors)
        return Response(data=data)


class CheckPolisAPIView(APIView):
    def get(self, request):
        report = Report.objects.all()
        serializer = ReportSerializer(report, many=True)
        return Response(data=serializer.data)

    @transaction.atomic
    def post(self, request):
        report = Report.objects.filter(polis_number=request.data['polis_number'])
        if report.exists():
            serializer = ReportSerializer(report, many=True)
            return Response(serializer.data)
        else:
            data = {
                "result": 5,
                "result_message": "Полис не найден в базе данных"
            }


            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


# Polis_end sanani aniqlash
def get_polis_end(payment_date):
    polis_end = datetime.strptime(payment_date, "%Y-%m-%d").date() + relativedelta(years=1) - timedelta(1)
    return polis_end



# InitiateTransanction update report
def initiate_report(serializer, data, transaction_id):
    init_report = Report.objects.filter(transaction_id=transaction_id).update_or_create(
        transaction_id = transaction_id,
        insurance_cost = serializer.data['insurance_cost'],
        insurance_premium = data['insurance_premium'],
        insurance_liability = data['insurance_liability'],
        agent_id = serializer.data['agent_id'],
        agent_phone = serializer.data['agent_phone'],
        product_id = serializer.data['product_id'],
        client_name = serializer.data['client_name'],
        client_address = serializer.data['client_address'],
        client_phone = serializer.data['client_phone'],
        client_passport = serializer.data['client_passport'],
        beneficiary_name = serializer.data['beneficiary_name'],
        polis_owner=f"{serializer.data['beneficiary_name']}, {serializer.data['client_name']}, {serializer.data['client_passport']}, {serializer.data['client_address']}, {serializer.data['client_phone']}",

        result = data['result'],
        result_message = data['result_message']
    )
    return init_report


# PerformTransanction update report
def perform_report(serializer, data, transaction_id):
    per_report = Report.objects.filter(transaction_id=transaction_id).update(
        polis_sery = data['polis_sery'],
        polis_number = data['polis_number'],
        polis_begin = data['polis_begin'],
        polis_end=data['polis_end'],
        polis_status="Выдан",
        qrcode = data['qrcode_url'],
        pdf = data['pdf'],

        result=data['result'],
        result_message=data['result_message']
    )
    return per_report


# TerminationTransanction update report
def termination_report(serializer, data, polis_number):
    term_report = Report.objects.filter(polis_number=polis_number).update(
        term_date = serializer.data['term_date'],
        term_note = serializer.data['term_note'],
        term_amount=data['term_amount'],
        polis_status="Расторгнут",

        result=data['result'],
        result_message=data['result_message']
    )
    return term_report

# QR-CODE generation
def gen_qrcode(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )


    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # img = qrcode.make(url)
    # type(img)  # qrcode.image.pil.PilImage

    return qr_img