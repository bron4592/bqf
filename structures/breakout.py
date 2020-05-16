from home.models import search
from . models import struct, invalid
import requests
import json
import pandas as pd
import requests
import io
from multiprocessing.pool import ThreadPool
from datetime import timedelta

def deleteAll():
	temp = struct.objects.all()
	temp.delete()

def breakout():

    temp = search.objects.all()
    for each in temp:
        equities, interval = equity(each)
        urls = []
        for one in equities:
            urls.append(selection(interval, one))

        with ThreadPool(4) as p:
            p.map(take, urls)



def remove():
    querys = struct.objects.filter(valid=False)
    for each in querys:
        obj = invalid(idCode = each.idCode, date = each.date, exchange = each.exchange, eqName = each.eqName,
                        timeFrame = each.timeFrame, bVol = each.bVol, takeVol = each.takeVol, volDelt = each.volDelt, retracePer = each.retracePer,
                        perRemain = each.perRemain, abLength = each.abLength, c = each.c, takeout = each.takeout, direction = each.direction, abPer = each.abPer,
                        valid = False)
        obj.save()
        each.delete()

def quote(equity):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE' + '&symbol=' + equity + '&apikey=EG6MF3ZBXZ3TYEAQ'
    dat = requests.get(url).content
    data = json.loads(dat)
    return float(data["Global Quote"]["05. price"])

def multiValid():
    temp = list(struct.objects.all())
    with ThreadPool(4) as p:
        p.map(validities, temp)

def validities(temp):
    try:
        time, high, low, close, volume = lastBar(temp)
        valid, perRemain, abper, c = validity(temp, temp.abLength, temp.b, temp.c, temp.takeout, temp.direction, time, high, low, close, volume, temp.newTake)
        temp.perRemain = perRemain
        temp.valid = valid
        print(temp.eqName)
        temp.abPer = abper
        temp.c = c
        temp.save()
    except:
        print('Error: Validity Failed To Retrieve.')

def lastBar(temp):
    apiKey = '&apikey=EG6MF3ZBXZ3TYEAQ'
    if temp.timeFrame == '10min':
        apiKey = '&apikey=EG6MF3ZBXZ3TYEAQ'
        address = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
        symbol = '&symbol=' + temp.eqName
        compInterval = '&interval=5min'
        datatype = '&datatype=csv'
        url = address + symbol + compInterval + apiKey + datatype
        csv_data = requests.get(url).content
        dat = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), header=0, names=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
              index_col=0, parse_dates=True)
        data = dat.resample(temp.timeFrame).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
    else:
        if temp.timeFrame.lower() == 'daily':
            address = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
            symbol = '&symbol=' + str(temp.eqName)
            datatype = '&datatype=csv'
            url = address + symbol + apiKey + datatype
        else:
            address = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
            symbol = '&symbol=' + str(temp.eqName)
            compInterval = '&interval=' + temp.timeFrame
            datatype = '&datatype=csv'
            url = address + symbol + compInterval + apiKey + datatype
        csv_data = requests.get(url).content
        dat = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), header=0, names=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
                  index_col=0, parse_dates=True)
        data = dat.reindex(index=dat.index[::-1])
    time = data.index.tolist()
    op = data['open'].tolist()
    high = data['high'].tolist()
    low = data['low'].tolist()
    close = data['close'].tolist()
    volume = data['volume'].tolist()
    if temp.timeFrame.lower() == 'daily':
        logTime = time[-1].date()
    else:
        logTime = time[-2] - timedelta(hours=2)

    return logTime, high[-1], low[-1], close[-1], volume[-1]



def validity(temp, abLength, b, c, takeout, direction, time, high, low, close, volume, newTake):
    valids = True
    if direction == 'Uptrend':
        if c > low:
            c = low
        if close < b:
            newTake = True
        if newTake is True:
            if close > b:
                obj = struct(idCode = temp.bVol + volume, date = time, exchange = temp.exchange, 
                            eqName = temp.eqName, timeFrame = temp.timeFrame, bVol = temp.bVol, takeVol = volume, 
                            volDelt = volume - temp.bVol, retracePer = temp.retracePer, perRemain = temp.perRemain, 
                            abLength = temp.abLength, c = temp.c, b = temp.b, takeout = close, direction = temp.direction, 
                            abPer = round((float(temp.abLength) / close) * 100, 2), valid = temp.valid)
                obj.save()
                print('New Takeout')
        downLen = round(abs(takeout - low), 3)
        upLen = round(abs(high - c), 3)
        if downLen >= abLength:
            valids = False
            perRemain = 0
            abper = 0
        
        if upLen >= abLength:
            valids = False
            perRemain = 0
            abper = 0
          
    elif direction == 'Downtrend':
        if c < high:
            c = high
        if close > b:
            newTake = True
        if newTake is True:
            if b > close:
                obj = struct(idCode = temp.bVol + volume, date = time, exchange = temp.exchange, 
                            eqName = temp.eqName, timeFrame = temp.timeFrame, bVol = temp.bVol, takeVol = volume, 
                            volDelt = volume - temp.bVol, retracePer = temp.retracePer,perRemain = temp.perRemain, 
                            abLength = temp.abLength, c = temp.c, b = temp.b, takeout = close, direction = temp.direction, 
                            abPer = round((float(temp.abLength) / close) * 100, 2), valid = temp.valid)
                obj.save()
                print('New Takeout')
        downLen = round(abs(high - takeout), 3)
        upLen = round(abs(c - low), 3)  
        if downLen >= abLength:
            valids = False
            perRemain = 0
            abper = 0
    
        if upLen >= abLength:
            valids = False
            perRemain = 0
            abper = 0

    
    if downLen > upLen:
        perRemain = round((1 - (downLen / abLength)) * 100, 2)
    else:
        perRemain = round((1 - (upLen / abLength)) * 100, 2)
    abper = round((float(abLength) / close) * 100, 2)
    if valids is True:
        pass
    return valids, perRemain, abper, c


def gapValidity(interval, timeArr, time, volArr, takeVol, highArr, closeArr, lowArr, abLength, c, takeout, currentBar, b, direction):
    valids = True
    newTake = False
    for i in range(currentBar, len(highArr)):
        if direction == 'Uptrend':
            if c > lowArr[i]:
                c = lowArr[i]
            if closeArr[i] < b:
                newTake = True
            if newTake is True:
                if closeArr[i] > b:
                    takeout = closeArr[i]
                    takeVol = volArr[i]
                    if interval == 'Daily':
                        time = timeArr[i].date()
                    else:
                        time = timeArr[i-1] - timedelta(hours=2)
                    newTake = False
            downLen = round(abs(takeout - lowArr[i]), 3)
            upLen = round(abs(highArr[i] - c), 3)
            if downLen >= abLength:
                valids = False
                perRemain = 0
                abper = 0
                break
            if upLen >= abLength:
                valids = False
                perRemain = 0
                abper = 0
                break
        elif direction == 'Downtrend':
            if c < highArr[i]:
                c = highArr[i]
            if closeArr[i] > b:
                newTake = True
            if newTake is True:
                if b > closeArr[i]:
                    takeout = closeArr[i]
                    takeVol = volArr[i]
                    if interval == 'Daily':
                        time = timeArr[i].date()
                    else:
                        time = timeArr[i-1] - timedelta(hours=2)
                    newTake = False
            downLen = round(abs(highArr[i] - takeout), 3)
            upLen = round(abs(c - lowArr[i]), 3)  
            if downLen >= abLength:
                valids = False
                perRemain = 0
                abper = 0
                break
            if upLen >= abLength:
                valids = False
                perRemain = 0
                abper = 0
                break
    
    if downLen > upLen:
        perRemain = round((1 - (downLen / abLength)) * 100, 2)
    else:
        perRemain = round((1 - (upLen / abLength)) * 100, 2)
    abper = round((float(abLength) / closeArr[-1]) * 100, 2)
    if valids is True:
        print('Valid CS')
    return valids, perRemain, abper, takeout, c, takeVol, time



def equity(temp):
	equities = []
	if int(temp.specif) == 1:
		equities = [str(i) for i in temp.specificEq.split()]
	if int(temp.specif) == 2:
		equities = sp500
	if int(temp.specif) == 3:
		equities = nasdaq
	if int(temp.specif) == 4:
		equities = nyse
	if int(temp.specif) == 5:
		equities = amex
	interval = temp.timeFrame
	exchange = temp.exchange
	return equities, interval


def selection(interval, each):
    apiKey = '&apikey=EG6MF3ZBXZ3TYEAQ'
    if interval.lower() == 'daily':
        address = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
        symbol = '&symbol=' + str(each)
        datatype = '&datatype=csv'
        url = address + symbol + apiKey + datatype
        return url
    else:
        address = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
        symbol = '&symbol=' + str(each)
        compInterval = '&interval=' + interval
        datatype = '&datatype=csv'
        url = address + symbol + compInterval + apiKey + datatype
        return url


	

def take(url):
    try:
        # Initialize Ticker API for each symbol
        element, interval = name(url)
        # CSV data converted to lists
        if interval == '10min':
            apiKey = '&apikey=EG6MF3ZBXZ3TYEAQ'
            address = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
            symbol = '&symbol=' + element
            compInterval = '&interval=5min'
            datatype = '&datatype=csv'
            url = address + symbol + compInterval + apiKey + datatype
            csv_data = requests.get(url).content
            dat = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), header=0, names=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
                  index_col=0, parse_dates=True)
            data = dat.resample(interval).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
        else:
            csv_data = requests.get(url).content
            dat = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), header=0, names=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
                      index_col=0, parse_dates=True)
            data = dat.reindex(index=dat.index[::-1])
        time = data.index.tolist()
        op = data['open'].tolist()
        high = data['high'].tolist()
        low = data['low'].tolist()
        close = data['close'].tolist()
        volume = data['volume'].tolist()


        # Uptrend Pattern
        a_bar = low[0]
        a_found = False
        bar = 0

        while bar < len(op) - 1:

            if low[bar] < low[bar + 1]:

                down_swing = low[bar]

                if a_bar > down_swing:
                    if high[bar] > high[bar+1]:
                        a_bar = low[bar+1]
                    else:
                        a_bar = down_swing
                    b_bar = 0
                    lowTrace = []
                    a_found = True
                    b_found = False


            bar += 1
            while a_found is True:

                if bar >= len(op) - 2:
                    break

                if b_bar < close[bar] and b_found is True:

                    lowRe = min(lowTrace)
                    abLength = round(b_bar - a_bar, 3)
                    retrace = round((b_bar - lowRe) / abLength, 3)
                    if interval == 'Daily':
                        logTime = time[bar].date()
                    else:
                        logTime = time[bar-1] - timedelta(hours=2)
                    #percentRemain, valids = validity(abLength, lowRe, close[bar], quote(each))
                    valids, perRemain, abPer, takeout, c, takeVol, logTime = gapValidity(interval, time, logTime, volume, volume[bar], high, close, low, abLength, lowRe, close[bar], bar, b_bar, 'Uptrend')
                    if struct.objects.filter(date = logTime).filter(eqName = element).filter(timeFrame = interval).exists():
                        print('Valid Exists')
                    elif invalid.objects.filter(date = logTime).filter(eqName = element).filter(timeFrame = interval).exists():
                        print('Invalid Exists')
                    elif valids is False:
                        print('Failed Valid')
                    else:
                        obj = struct(idCode = bVolume+volume[bar], date = logTime, exchange = 'Equities', eqName = element,
                        timeFrame = interval, bVol = bVolume, takeVol = volume[bar], volDelt = volume[bar] - bVolume, retracePer = round(retrace*100, 3),
                        perRemain = perRemain, abLength = abLength, c = c, b = b_bar, takeout = takeout, direction = 'Uptrend', abPer = abPer,
                        valid = valids)
                        obj.save()
                        print(element + ': ' + interval)

                    
                    a_found = False
                    a_bar = 1000000

                    break

                if high[bar] > high[bar + 1]:
                    upSwing = high[bar]

                    if upSwing > b_bar:
                        b_bar = upSwing
                        bVolume = volume[bar]
                        b_found = True

                if a_bar >= low[bar]:
                    a_found = False
                    a_bar = 1000000
                    break

                elif b_found is True:
                    lowTrace.append(low[bar])

                bar += 1

        # Downtrend Pattern
        a_bar = high[0]
        a_found = False
        bar = 0

        while bar < len(op) - 1:

            if high[bar] > high[bar + 1]:

                down_swing = high[bar]

                if a_bar < down_swing:

                    if low[bar] < low[bar+1]:
                        a_bar = high[bar+1]
                    else:
                        a_bar = down_swing
                    b_bar = 100000
                    lowTrace = []
                    a_found = True
                    b_found = False
            bar += 1
            while a_found is True:
                if bar >= len(op) - 2:
                    break

                if b_bar > close[bar] and b_found is True:
                    lowRe = max(lowTrace)
                    abLength = round(abs(b_bar - a_bar), 3)
                    retrace = round(abs(b_bar - lowRe) / abLength, 3)
                    if interval == 'Daily':
                        logTime = time[bar].date()
                    else:
                        logTime = time[bar-1] - timedelta(hours=2)
                    #percentRemain, valids = validity(abLength, lowRe, close[bar], quote(each)) 
                    valids, perRemain, abPer, takeout, c, takeVol, logTime = gapValidity(interval, time, logTime, volume, volume[bar], high, close, low, abLength, lowRe, close[bar], bar, b_bar, 'Downtrend')
                    if struct.objects.filter(date = logTime).filter(eqName = element).filter(timeFrame = interval).exists():
                        print('Valid Exists')
                    elif invalid.objects.filter(date = logTime).filter(eqName = element).filter(timeFrame = interval).exists():
                        print('Invalid Exists')
                    elif valids is False:
                        print('Failed Valid')
                    else:
                        obj = struct(idCode = bVolume+volume[bar], date = logTime, exchange = 'Equities', eqName = element,
                        timeFrame = interval, bVol = bVolume, takeVol = volume[bar], volDelt = volume[bar] - bVolume, retracePer = round(retrace*100, 3),
                        perRemain = perRemain, abLength = abLength, c = c, b = b_bar, takeout = takeout, direction = 'Downtrend', abPer = abPer,
                        valid = valids)
                        obj.save()
                        print(element + ': ' + interval)
                    
                    a_found = False
                    a_bar = 0
                    break

                if low[bar] < low[bar + 1]:
                    upSwing = low[bar]

                    if upSwing < b_bar:
                        b_bar = upSwing
                        bVolume = volume[bar]
                        b_found = True

                if a_bar <= high[bar]:
                    a_found = False
                    a_bar = 0
                    break

                elif b_found is True:
                    lowTrace.append(high[bar])

                bar += 1

    except:
        print('Error: Structure Failed To Retrieve.')

def name(url):
    element = ''
    interval = ''
    if url[43:60] == 'TIME_SERIES_DAILY':
        for i in range(68, len(url)):
            if url[i] == '&':
                break
            element += url[i]
        interval = 'Daily'
    else:
        for i in range(71, len(url)):
            if url[i] == '&':
                for j in range(i+10, len(url)):
                    if url[j] == '&':
                        break
                    interval += url[j]
                break
            element += url[i]
    return element.upper(), interval


'''
frame = ((0, '0min'), (1, '1min'), (2, '2min'), (3, '3min'), (4, '4min'), (5, '5min'), 
	(6, '6min'), (7, '7min'), (8, '8min'),(9, '9min'),
	(10, '10min'),(15, '15min'),(20, '20min'),(25, '25min'),(30, '30min'),
	(35, '35min'),(40, '40min'),(45, '45min'),(50, '50min'),(55, '55min'),
	(60, '60min'),(90, '90min'),('2hr', '2hr'),
	('3hr', '3hr'),('4hr','4hr'),('1d', '1 Day'),('1week', '1 Week'),('1month','1 Month'))
'''



#STOCK EXCHANGES

nas = pd.read_csv("NASDAQ.csv")
nasdaq = nas['Symbol'].tolist()
ny = pd.read_csv("NYSE.csv")
nyse = ny['Symbol'].tolist()
am = pd.read_csv("AMEX.csv")
amex = am['Symbol'].tolist()
sp500 = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AMG', 'AFL', 'A', 'APD',
         'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'AGN', 'ADS', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN',
         'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI',
         'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'AIV', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ARNC', 'ANET', 'AJG', 'AIZ', 'T',
         'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BHGE', 'BLL', 'BAC', 'BK', 'BAX', 'BBT', 'BDX', 'BRK.B', 'BBY', 'BIIB',
         'BLK', 'HRB', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BHF', 'BMY', 'AVGO', 'BR', 'BF.B', 'CHRW', 'COG',
         'CDNS', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CAT', 'CBOE', 'CBRE', 'CBS', 'CELG', 'CNC', 'CNP', 'CTL', 'CERN',
         'CF', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS',
         'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'COO', 'CPRT',
         'GLW', 'COST', 'COTY', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN',
         'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DOV', 'DWDP', 'DTE', 'DRE', 'DUK', 'DXC', 'ETFC',
         'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR',
         'ESS', 'EL', 'EVRG', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT',
         'FDX', 'FIS', 'FITB', 'FE', 'FISV', 'FLT', 'FLIR', 'FLS', 'FLR', 'FMC', 'FL', 'F', 'FTV', 'FBHS', 'BEN', 'FCX',
         'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GS', 'GT', 'GWW', 'HAL', 'HBI', 'HOG',
         'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HP', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HFC', 'HOLX', 'HD', 'HON', 'HRL',
         'HST', 'HPQ', 'HUM', 'HBAN', 'HII', 'IDXX', 'INFO', 'ITW', 'ILMN', 'IR', 'INTC', 'ICE', 'IBM', 'INCY', 'IP',
         'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JEC', 'JBHT', 'JEF', 'SJM', 'JNJ', 'JCI', 'JPM',
         'JNPR', 'KSU', 'K', 'KEY', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KHC', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LEG',
         'LEN', 'LLY', 'LNC', 'LKQ', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM',
         'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT',
         'MAA', 'MHK', 'TAP', 'MDLZ', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'MYL', 'NDAQ', 'NOV', 'NKTR', 'NTAP',
         'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC',
         'NCLH', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'PCAR', 'PKG', 'PH', 'PAYX', 'PYPL', 'PNR',
         'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'RL', 'PPG', 'PPL', 'PFG',
         'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RJF', 'RTN', 'O', 'RHT',
         'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROP', 'ROST', 'RCL', 'CRM', 'SBAC', 'SLB',
         'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SPGI', 'SWK', 'SBUX', 'STT', 'SRCL',
         'SYK', 'STI', 'SIVB', 'SYMC', 'SYF', 'SNPS', 'SYY', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'FTI', 'TXN', 'TXT',
         'TMO', 'TIF', 'TWTR', 'TJX', 'TMK', 'TSS', 'TSCO', 'TDG', 'TRV', 'TRIP', 'FOXA', 'FOX', 'TSN', 'UDR', 'ULTA',
         'USB', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN',
         'VRSK', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WDC',
         'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBH', 'ZION',
         'ZTS']
