import asyncio
import tornado.web
from router import routers

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        data = {'code' : 0,'message':""}

async def main():
    application = tornado.web.Application(routers)
    application.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())