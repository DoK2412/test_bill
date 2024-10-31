import uuid
import requests


from fastapi import status
from fastapi.responses import JSONResponse


from lago_python_client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Customer, Wallet, WalletTransaction

from settings import customers, wallets, wallet_transactions, plans
from loggins.logger import logger


async def new_user(request):
    """
    Функция создания нового пользователя
    :param request: параметры внутри запроса
    :return: external_id идентификатор пользователя
    """
    try:

        client = Client(api_key=request.headers.get('Authorization').split('Bearer ')[1],
                        api_url=customers)

        customer = Customer(
            external_id=str(uuid.uuid4()))

        try:
            result_user = client.customers.create(customer)
            if result_user.status_code == 200:
                if result_user.get('customer'):
                    return result_user.json()['customer']['external_id']
                    # response.set_cookie(key="user_id", value=str(result_user.json()['customer']['external_id']), samesite=None,
                    #                     secure=False)
                else:
                    return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})
            else:
                return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})
        except LagoApiError as e:
            logger.exception(f"Ошибка стороннего сервиса {e.status_code}")
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


async def creating_wallet(request, external_id):
    """
    Функция создания кошелька пользователю
    :param request: параметры внутри запроса
    :param external_id: идентификатор пользователя
    :return: bool значение результата выполнения
    """
    try:
        client = Client(api_key=request.headers.get('Authorization').split('Bearer ')[1],
                        api_url=wallets)
        wallet = Wallet(
            rate_amount='1.5',
            currency='RUB',
            expiration_at='2025-07-07T23:59:59Z',
            external_customer_id=external_id
        )
        result_wallet = client.wallets.create(wallet)
        if result_wallet.status_code == 200:
            return True
        else:
            return False

    except LagoApiError as e:
        logger.exception(f"Ошибка стороннего сервиса {e.status_code}")


async def getting_user(request, external_id):
    """
    Функция получние пользователя
    :param request: параметры внутри запроса
    :param external_id: идентификатор пользователя
    :return: lago_id пользователя
    """
    try:
        client = Client(api_key=request.headers.get('Authorization').split('Bearer ')[1],
                        api_url=customers)
        user_data = client.customers.find(external_id)

        if user_data.status_code == 200:
            result = user_data.json()
            if result.get('customer'):
                return result['customer']['lago_id']
            else:
                return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})

    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


async def get_user_wallet(request, lago_id):
    """

    :param request: параметры внутри запроса
    :param lago_id: идентификатор пользователя
    :return: сведения о кошельке пользователя
    """
    try:
        client = Client(api_key=request.headers.get('Authorization').split('Bearer ')[1],
                        api_url=wallets)
        result_wallets = client.wallets.find(lago_id)
        if result_wallets.status_code == 200:
            result = result_wallets.json()
            if result.get('wallet'):
                return result_wallets
        else:
            return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


async def replenishment_balance(request, wallet_id, credits):
    """
    Функция пополнения пошелька пользователя
    :param request: параметры внутри запроса
    :param wallet_id: идентификатор кошелька пользователя
    :param credits: сумма на пополнение
    :return: результат выполнения
    """
    try:
        client = Client(api_key=request.headers.get('Authorization').split('Bearer ')[1],
                                    api_url=wallet_transactions)
        transaction = WalletTransaction(
            wallet_id=wallet_id,
            paid_credits=str(credits),
            granted_credits='10.0'
            )
        result = client.wallet_transactions.create(transaction)
        if result.status_code == 200:
            return JSONResponse(content={status.HTTP_200_OK: "пополнение прошло успешно."})
        else:
            return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


async def creation_plan(request):
    """
    Функция создания плана пользователя
    :param request: параметры внутри запроса
    :return: результат выполнеия
    """
    try:
        payload = {"plan": {
            "name": "test",
            "invoice_display_name": "Test plan",
            "code": "test",
            "interval": "monthly",
            "description": "Test plan.",
            "amount_cents": 1000,
            "amount_currency": "RUB",
            "trial_period": 10,
            "pay_in_advance": True,
            "bill_charges_monthly": None,
            "tax_codes": ["russian_standard_vat"],
            "minimum_commitment": {
                "amount_cents": 10000,
                "invoice_display_name": "Minimum Commitment (C1)",
                "tax_codes": ["russian_standard_vat"]
                 }
                }
            }
        headers = {
            "Authorization": f"{request.headers.get('Authorization').split('Bearer ')[1]}",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", plans, json=payload, headers=headers)
        if response.status_code == 200:
            return JSONResponse(content={status.HTTP_200_OK: "Пользователь успешно создан.."})
    except Exception as e:
        return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})

