# -*- coding: utf-8 -*-
import os
import sys
import web3
import django
import datetime
import random
import time

from datetime import timedelta
from django.utils import timezone

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dice.settings")
django.setup()

from web3 import Web3, Account
from web3.providers.rpc import HTTPProvider

import logging
logger = logging.getLogger(__name__)

from dice.models import Bets

from web3.auto import w3



def home(request):

    # XXX TODO filter for paired transactions (status=1, tx_hash and player is not empty)
    #games = Bets.objects.filter(status=True,).order_by('-pk')[:100]
    temp_games = Bets.objects.filter().order_by('-pk')[:100]

    # XXX TODO my_games = Bets.objects.filter(player=player_wallet).order_by('-pk')

    response = render(
        request=request,
        template_name='index.html',
        context={
            'contract': settings.ETHEREUM_DICE_CONTRACT,
            'contract_abi': settings.ETHEREUM_DICE_CONTRACT_ABI,
            'games': temp_games,
            },
    )

    return response

def get_game_abi(request):

    return HttpResponse(settings.ETHEREUM_DICE_CONTRACT_ABI)


def get_game_contract(request):

    if('ropsten' in settings.ETHEREUM_PROVIDER_HOST):
        etherscan_url = "https://ropsten.etherscan.io/address/"+settings.ETHEREUM_DICE_CONTRACT
    else:
        etherscan_url = "https://etherscan.io/address/"+settings.ETHEREUM_DICE_CONTRACT

    return HttpResponseRedirect(etherscan_url)


def get_clock(request):

    print('ajax_get_clock')

    now = datetime.datetime.now(tz=timezone.utc).isoformat()

    return JsonResponse({'clock': now})


def ajax_bet(request):
    
    player_wallet = request.POST.get('wallet')
    bet_tx_hash = request.POST.get('value')
    bet_amount = request.POST.get('amount')

    bet_numbers = request.POST.getlist('numbers[]')

    _bet_numbers = []
    for _number in  bet_numbers:
        _bet_numbers.append(int(_number))
    bet_numbers = _bet_numbers

    Bets.objects.create(
        player = player_wallet,
        tx_hash = bet_tx_hash,
        amount = bet_amount,
        numbers = str(bet_numbers),
    )
    print('ajax_bet')
    print('player_wallet', player_wallet)
    print('bet_tx_hash', bet_tx_hash)
    print('bet_amount', bet_amount)
    print('bet_numbers', bet_numbers)

    return HttpResponse('Ok')


def ajax_my_games(request):
    # XXX todo filter my games
    return HttpResponse('xxx todo filter my games')

def ajax_games(request):
    bets = Bets.objects.all().order_by('-pk')[:100]
    return JsonResponse(bets, safe=False)

