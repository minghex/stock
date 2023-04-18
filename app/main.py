import asyncio
import tornado.web
from router import routers

async def main():
    application = tornado.web.Application(routers)
    application.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())