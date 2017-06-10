'''
Created on 4. lip 2017.

@author: eaneivc
'''
BOT_NAME = 'carspider'

ITEM_PIPELINES = {
	'carspider.pipelines.CarAddDbPipeline' : 100
	}

SPIDER_MODULES = ['carspider.main']

LOG_LEVEL = 'INFO'
LOG_FILE = 'error.log'
LOG_ENABLED = True
