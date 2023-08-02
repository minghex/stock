import tornado.ioloop
import tornado.web
from motor.motor_tornado import MotorClient
from router.router import routers

if __name__ == "__main__":
    # 创建 MotorClient 对象并连接到 MongoDB
    client = MotorClient('mongodb://172.17.0.1:27017')
    db = client['test_stock']

    # 获取要操作的集合对象
    collection = db['test_collection']

    # 创建 Tornado 应用程序对象，并将集合对象传递给基类
    application = tornado.web.Application(routers, collection=collection)

    # 启动应用程序监听端口
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()