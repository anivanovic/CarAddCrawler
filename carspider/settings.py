'''
Created on 4. lip 2017.

@author: eaneivc
'''
BOT_NAME = 'carspider'

ITEM_PIPELINES = {
	'carspider.pipelines.CarAddDbPipeline' : 100
	}

SPIDER_MODULES = ['carspider.main']

LOG_LEVEL = 'DEBUG'
LOG_FILE = 'error.log'
LOG_ENABLED = True
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
