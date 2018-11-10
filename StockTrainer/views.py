from django.http import JsonResponse
from django.shortcuts import render
from .utils import *


# Create your views here.
def index(request):
    context = {
        "stock_symbols": sp500
    }
    return render(request, 'StockTrainer/index.html', context)


def stock(request):
    stock_symbol = request.GET.get('stock_symbol').strip()
    client = get_influxdb_client()
    prices = query(client, stock_symbol)
    print(stock_symbol, len(stock_symbol))
    result = list(prices.get_points('price'))
    return JsonResponse(result, safe=False)


def import_portfolio(request):
    return render(request, 'StockTrainer/import_portfolio.html')