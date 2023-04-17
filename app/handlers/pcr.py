from handlers.base import BaseHandler
import json

# import model.pcr as pcr

class PCRHandler(BaseHandler):
    def get(self):
        my_data = {'code': 0, 'foo': 'bar', 'baz': [1, 2, 3]}
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(my_data))