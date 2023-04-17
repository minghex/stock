from handlers.home import HomeHandler
from handlers.pcr import PCRHandler

routers = [
    (r'/', HomeHandler),
    (r'/pcr', PCRHandler),
]