from fastapi import APIRouter, Request, Response, Query, status
from fastapi.responses import JSONResponse


from loggins.logger import logger
from service.rout_schemes import Withdraw, Deposit

import service.auxiliary_functions as af

service_router = APIRouter(prefix="/users")


@service_router.post('')
async def create_user(request: Request, response: Response):
    try:
        if request.headers.get('Authorization'):
            user_id = await af.new_user(request)
            if isinstance(user_id, str):
                user_wallet = await af.creating_wallet(request, user_id)
                if user_wallet:
                    plan = await af.creation_plan(request)
                    return plan
                else:
                    return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Ошибка валидации параметрво."})
            else:
                return user_id
        else:
            return JSONResponse(content={status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED."})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


@service_router.post('/withdraw')
async def get_withdraw(request: Request,
                       withdraw: Withdraw):
    try:
        if request.headers.get('Authorization'):
            user_lago_id = await af.getting_user(request, withdraw.user_id)
            if isinstance(user_lago_id, str):
                user_wallet = await af.get_user_wallet(request, user_lago_id)
                if user_wallet.json()['wallet']['balance_cents'] > withdraw.amount:
                    pass
                else:
                    return JSONResponse(content={status.HTTP_400_BAD_REQUEST: "Недостаточно средств на счете."})

            else:
                return JSONResponse(content={status.HTTP_404_NOT_FOUND: "Пользователь не найден."})
        else:
            return JSONResponse(content={status.HTTP_401_UNAUTHORIZED: "Доступ ограничен."})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


@service_router.get('/balance')
async def post_balance(request: Request,
                       user_id: str = Query(description="Уникальный идентификатор кошелька.")):
    try:
        if request.headers.get('Authorization'):
            user_lago_id = await af.getting_user(request, user_id)
            if isinstance(user_lago_id, str):
                user_wallet = await af.get_user_wallet(request, user_id)
                return {"Балланс:": user_wallet.json()['wallet']['balance_cents']}

            else:
                return JSONResponse(content={status.HTTP_404_NOT_FOUND: "Пользователь не найден."})
        else:
            return JSONResponse(content={status.HTTP_401_UNAUTHORIZED: "Доступ ограничен."})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")


@service_router.post('/deposit')
async def post_deposit(request: Request,
                       deposit: Deposit):
    try:
        if request.headers.get('Authorization'):
            user_lago_id = await af.getting_user(request, deposit.user_id)
            if isinstance(user_lago_id, str):
                user_wallet = await af.get_user_wallet(request, user_lago_id)
                deposit = await af.replenishment_balance(request, user_wallet.json()['wallet']['lago_id'], deposit.amount)
                return deposit

            else:
                return JSONResponse(content={status.HTTP_404_NOT_FOUND: "Пользователь не найден."})
        else:
            return JSONResponse(content={status.HTTP_401_UNAUTHORIZED: "Доступ ограничен."})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении процесса {e}")
