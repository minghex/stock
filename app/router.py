from handlers.home import HomeHandler
from handlers.pcr import OptionPCRHandler 

routers = [
    (r'/', HomeHandler),
    (r'/option', OptionPCRHandler),
]