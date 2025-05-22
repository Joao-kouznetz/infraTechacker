# query_service/main.py
from fastapi import FastAPI, Depends, APIRouter
from security import get_current_active_user  # Importa a função de validação de token
from schema import (
    UserDataFromToken,
)  # Importa o schema para os dados do usuário do token
import yfinance as yf

app = FastAPI(title="Query Service")
router_query = APIRouter(prefix="/query", tags=["Data Queries"])


def get_ticker_data_logic():
    ticker_symbol = "T"  # Exemplo: AT&T
    try:
        ticker = yf.Ticker(ticker_symbol)
        historical_data = ticker.history(period="5d")
        if historical_data.empty:
            return f"Nenhum dado encontrado para o ticker {ticker_symbol} nos últimos 5 dias."

        close_prices = historical_data["Close"]
        result = "\n".join(
            [
                f"{date.strftime('%Y-%m-%d')}: ${price:.2f}"
                for date, price in close_prices.items()
            ]
        )
        return f"Dados de fechamento da empresa {ticker_symbol} (últimos 5 dias):\n{result}"
    except Exception as e:
        return f"Erro ao buscar dados para {ticker_symbol}: {str(e)}"


@router_query.get("/consultar")
async def get_data_consulta(
    current_user: UserDataFromToken = Depends(get_current_active_user),
):
    # current_user contém os dados validados do token (ex: email)
    # Você pode usar current_user.email se precisar, por exemplo, para logging
    ticker_info = get_ticker_data_logic()
    return {"user_email": current_user.email, "data": ticker_info}


app.include_router(router_query)


@app.get("/")
async def root_query():
    return {"message": "Query Service is running"}
