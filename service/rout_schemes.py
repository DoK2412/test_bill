from pydantic import BaseModel
from fastapi import Query


class Withdraw(BaseModel):
    user_id: str = Query(description="уникальный идентификатор пользователя.")
    amount: int = Query(description="кол-во токенов для списания.")
    type: str = Query(description="тип транзакции (output input)")


class Deposit(BaseModel):
    user_id: str = Query(description="уникальный идентификатор пользователя.")
    amount: int = Query(description="кол-во токенов для списания.")
