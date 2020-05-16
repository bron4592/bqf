from home.models import watch, hotlist
from structures.models import struct, trade
import pandas as pd
import io
import requests
import json
from multiprocessing.pool import ThreadPool
import datetime


def querys():
   temp = watch.objects.all()
   querys = []
   for each in temp:
      queryset = struct.objects.filter(timeFrame=each.timeFrame)
      if each.retracePer is not None:
         queryset = struct.objects.filter(retracePer__lte=each.retracePer)
      if each.perRemain is not None:
         queryset = queryset.filter(perRemain__gte=each.perRemain)
      if each.abPer is not None:
         queryset = queryset.filter(abPer__gte=each.abPer)
      if each.volDelt is not None:
         if each.volDelt is True:
            queryset = queryset.filter(volDelt__gte=1)
         if each.volDelt is False:
            queryset = queryset.filter(volDelt__lte=-1)
      for each in queryset:
         querys.append(each)
   return querys
 



def equity(temp):
	equities = []
	if int(temp.specif) == 1:
		equities = [str(i).upper() for i in temp.specificEq.split()]
	if int(temp.specif) == 2:
		equities = sp500
	if int(temp.specif) == 3:
		equities = nasdaq
	if int(temp.specif) == 4:
		equities = nyse
	if int(temp.specif) == 5:
		equities = amex
	return equities

def hotRSI():
   temp = querys()
   with ThreadPool(10) as p:
      p.map(getRsi, temp)


def getRsi(query):
   try:
      frame = ['1min','5min','15min','30min','60min','daily']
      equity = query.eqName
      time = query.timeFrame
      if time.lower() == 'daily':
         frame = frame[2:6]
      if time == '60min':
         frame = frame[1:5]
      if time =='30min':
         frame = frame[:4]
      if time == '15min':
         frame = frame[:3]
      if time == '10min':
         frame = frame[:2]
      if time == '5min':
         frame = frame[:2]
      if time == '1min':
         frame = frame[:1]
      for i in range(len(frame)):
         if trade.objects.filter(eqName=equity, childtime=frame[i], parTime=time).exists():
            print('Exists')
         else:

            print('Created rsi obj')

            url = 'https://www.alphavantage.co/query?function=RSI&symbol='+ equity + '&interval=' + frame[i] +\
                '&time_period=14&series_type=close&datatype=csv&apikey=EG6MF3ZBXZ3TYEAQ'
            csv_data = requests.get(url).content
            data = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), header=0)
            rsi = data['RSI'].tolist()
            latest = rsi[0]

            obj = trade(eqName=equity, date=query.date, childtime=frame[i], parTime=time, indicator = 'RSI', current=latest, thresh = 0, direction = query.direction)
            obj.save()
   except:
      print('Error: RSI failed to retrieve.')

def inHot():
   temp = trade.objects.all()
   with ThreadPool(8) as p:
      p.map(RSI, temp)
   thresh()

def RSI(temp):
      url = 'https://www.alphavantage.co/query?function=RSI&symbol='+ temp.eqName + '&interval=' + temp.childtime +\
          '&time_period=14&series_type=close&datatype=csv&apikey=EG6MF3ZBXZ3TYEAQ'
      csv_data = requests.get(url).content
      data = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), header=0)
      rsi = data['RSI'].tolist()
      temp.current = rsi[0]
      temp.save()
      print('Success')


def rsiQuery():
   temp = hotlist.objects.all()
   querys = []
   for each in temp:
      if each.maxormin is True:
         queryset = trade.objects.filter(childtime='1min', current__gte=each.value1)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value1
            i.save()
         queryset = trade.objects.filter(childtime='5min', current__gte=each.value2)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value2
            i.save()
         queryset = trade.objects.filter(childtime='15min', current__gte=each.value3)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value3
            i.save()
         queryset = trade.objects.filter(childtime='30min', current__gte=each.value4)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value4
            i.save()
         queryset = trade.objects.filter(childtime='60min', current__gte=each.value5)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value5
            i.save()
         queryset = trade.objects.filter(childtime='daily', current__gte=each.value6)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value6
            i.save()
      if each.maxormin is False:
         queryset = trade.objects.filter(childtime='1min', current__lte=each.value1)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value1
            i.save()
         queryset = trade.objects.filter(childtime='5min', current__lte=each.value2)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value2
            i.save()
         queryset = trade.objects.filter(childtime='15min', current__lte=each.value3)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value3
            i.save()
         queryset = trade.objects.filter(childtime='30min', current__lte=each.value4)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value4
            i.save()
         queryset = trade.objects.filter(childtime='60min', current__lte=each.value5)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value5
            i.save()
         queryset = trade.objects.filter(childtime='daily', current__lte=each.value6)
         for i in queryset:
            querys.append(i)
            i.thresh = each.value6
            i.save()
      
   return querys


def thresh():
   temp = trade.objects.all()
   hots = hotlist.objects.all()
   for each in hots:
      queryset = trade.objects.filter(childtime='1min', current__gte=each.value1)
      for i in queryset:
         i.thresh = each.value1
         i.save()
      queryset = trade.objects.filter(childtime='5min', current__gte=each.value2)
      for i in queryset:
         i.thresh = each.value2
         i.save()
      queryset = trade.objects.filter(childtime='15min', current__gte=each.value3)
      for i in queryset:
         i.thresh = each.value3
         i.save()
      queryset = trade.objects.filter(childtime='30min', current__gte=each.value4)
      for i in queryset:
         i.thresh = each.value4
         i.save()
      queryset = trade.objects.filter(childtime='60min', current__gte=each.value5)
      for i in queryset:
         i.thresh = each.value5
         i.save()
      queryset = trade.objects.filter(childtime='daily', current__gte=each.value6)
      for i in queryset:
         i.thresh = each.value6
         i.save()
'''
eqName = models.CharField(max_length=100)
   date = models.DateTimeField()
   childtime = models.CharField(max_length=100)
   parTime = models.CharField(max_length=100)
   indicator = models.CharField(max_length=100)
   current = models.FloatField()
   thresh = models.FloatField()
   valid = models.BooleanField(default=True)
'''








'''
STRUCT

idCode = models.CharField(max_length=100)
date = models.DateTimeField()
exchange = models.CharField(max_length=100)
eqName = models.CharField(max_length=100)
timeFrame = models.CharField(max_length=100)
bVol = models.IntegerField()
takeVol = models.IntegerField()
volDelt = models.IntegerField()
retracePer = models.FloatField()
perRemain = models.FloatField()
direction = models.CharField(max_length=100)
abPer = models.FloatField()
abLength = models.FloatField()
c = models.FloatField()
takeout = models.FloatField()
valid = models.BooleanField(default=True)



WATCH

watchName = models.CharField(max_length=100)
specif = models.IntegerField()
specificEq = models.CharField(max_length=100, blank=True, default='')
timeFrame = models.CharField(max_length=100)
retracePer = models.FloatField()
perRemain = models.FloatField()
abPer = models.FloatField()
volDelt = models.IntegerField()
author = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
date = models.DateTimeField(auto_now=True)
description = models.CharField(max_length=200)
'''
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