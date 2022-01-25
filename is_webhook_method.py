from config import config

webhook_method = True if config['GENERAL']['WEBHOOK_METHOD'] == 'True' else False
