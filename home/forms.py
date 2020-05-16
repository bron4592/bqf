from django import forms
from . import models

	
exchanges = (
		('EQ','Equities' ),
		('FX','Forex'),
		('Bonds', 'Bonds'), 
		('Crypto', 'Crypto'),
		)

bools = ((True, 'Yes'), 
		(False, 'No'))

sender = ((True, 'Active Database'), (False, 'Backtesting Database'))

frame = (('1min', '1min'), ('5min', '5min'),('10min', '10min'),('15min', '15min'),('30min', '30min'),('60min', '60min'),('Daily','Daily'))
presets = (
		(1, "Custom Search"),
		(2, "S&P 500"),
		(3, "NASDAQ"),
		(4, "NYSE"),
		(5, "AMEX"),
	)
presets1 = (
		(0, "All Structures"),
		(1, "Custom Search"),
		(2, "S&P 500"),
		(3, "NASDAQ"),
		(4, "NYSE"),
		(5, "AMEX"),
	)
indicators = (
		('RSI', 'RSI'),
		('MACD', 'MACD')
	)
maxormin = (
		(True, 'Greater Than or Equal to'),
		(False, 'Less Than or Equal to')
	)
vols = (
		(True, 'Takeout > B Point'),
		(False, 'B Point > Takeout'),
		(None, 'Any Delta'),

	)

class newSearch(forms.ModelForm):
	"""docstring for search"""
	class Meta:
		model = models.search
		fields = ['searchName', 'exchange', 'specif','specificEq','timeFrame', 
		 'send', ]
		labels = {
			'searchName':'Name of Search', 'timeFrame':'Select a Time Frame', 
			 'send':'Send To', 'specificEq':'List Specific Equities (Custom Search Must Be Selected, Separate Symbols By Spaces)',
			 'specif':'Choose Pre-set Search or Custom Equities'
		}
		widgets = { 
			'timeFrame': forms.Select(choices=frame), 
			'exchange': forms.Select(choices=exchanges),
			'keep': forms.Select(choices=bools),
			'send': forms.Select(choices=sender),
			'specif': forms.Select(choices=presets),
		}

		verbose_name_plural = 'Searches'

class newWatch(forms.ModelForm):

	class Meta:
		model = models.watch
		fields = ['watchName', 'specif', 'specificEq', 'timeFrame', 'retracePer', 'abPer', 'perRemain', 'volDelt',]
		labels = {
			'watchName': 'Watchlist Name', 'specificEq':'List Specific Equities (Custom Search Must Be Selected, Separate Symbols By Spaces)',
			'retracePer':'Retracement Percentage Maximum', 
			'perRemain':'Percent Extension Left To Achieve Minimum', 'volDelt':'Volume Delta',
			'timeFrame':'Select a Time Frame','specif':'Choose Pre-set Search or Custom Equities', 
			'abPer':'AB Leg as Percent of Price Minimum',
		}
		widgets = {
			'timeFrame': forms.Select(choices=frame),
			'specif': forms.Select(choices=presets1),
			'volDelt': forms.Select(choices=vols),
		}
class newHot(forms.ModelForm):
	
	class Meta:
		model = models.hotlist
		fields = ['hotName','maxormin','value1','value2','value3','value4','value5','value6',]
		labels = {'hotName': 'Hotlist Name', 'maxormin': 'Target Values Greater Than or Less Than', 'value1':'RSI Target For 1min Child',
				 'value2':'RSI Target For 5min Child', 'value3':'RSI Target For 15min Child', 'value4':'RSI Target For 30min Child',
				  'value5':'RSI Target For 60min Child', 'value6':'RSI Target For Daily Child',
					}
		widgets = {
				'maxormin': forms.Select(choices=maxormin)
		}

			
		