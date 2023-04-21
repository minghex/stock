import tornado.web
import json

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header('Content-Type', 'application/json')

    def prepare(self):
        pass
        # 请求处理之前执行
        # try:
        #     self.request_data = json.loads(self.request.body)
        # except ValueError:
        #     self.write_response(400,"Invalid request body")
        #     self.finish()
        

    def on_finish(self):
        # 请求处理结束之后执行
        pass

    def write_response(self, code, message, data=None):
        response = {"code": code, "message": message}
        if data is not None:
            response["data"] = data
        self.finish(json.dumps(response))

    def write_success_response(self, data=None):
        self.write_response(0, "OK", data) 