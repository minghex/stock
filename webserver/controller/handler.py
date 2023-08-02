import tornado.ioloop
import tornado.web
import json
import time

Response_Success_Code = 0
Response_ReqError_Code = 1


data_cache_dict = {}

class BaseHandler(tornado.web.RequestHandler):
    async def update(self, collection, filter, update):
        result = await collection.update_one(filter, update, upsert=True)
        return result.modified_count

    async def find(self, collection, filter):
        cursor = collection.find(filter)
        results = []
        async for document in cursor:
            results.append(document)
        return results

    async def find_one(self, collection, filter):
        document = await collection.find_one(filter)
        return document
    
    async def get_data_from_database(self, key) -> str:
        cache_data = await self.get_data_from_cache(key)
        if not cache_data:
            return await self.get_data_from_db(key)
        return cache_data
    
    async def get_data_from_cache(self, key) -> str:
        global data_cache_dict
        if key in data_cache_dict:
            return data_cache_dict[key]['data_str']
        else:
            return None

    async def get_data_from_db(self, key) -> str:
        collection = self.settings['collection']
        document = await self.find_one(collection, {'key': key})
        if not document:
            return None
        else:
            return document['data_str']
    
    async def save_data_to_db(self, key:str, data:str, freshCache=True):
       collection = self.settings['collection']
       modified_count = await self.update(collection, {'key': key}, {'$set': {'data_str': data}}) 
       if freshCache:
           data_cache_dict[key] = {'data_str': data}
       return modified_count


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header('Content-Type', 'application/json')
    
    # 解析Request数据
    def get_json_body(self):
        try:
            request_body = self.request.body
            json_data = json.loads(request_body)
            return json_data
        except (json.JSONDecodeError, ValueError):
            # 当请求的内容无法解析为JSON时，可能会抛出异常
            # 这里可以根据需求进行异常处理
            return None

    # 请求处理前
    def perpare(self):
        pass

    # 请求处理后
    def on_finish(self):
        pass

    def write_response(self, code, message, data=None):
        response = {"code": code, "message": message}
        if data is not None:
            response["data"] = data
        self.finish(json.dumps(response))

    def write_success_response(self, data=None):
        self.write_response(0, "OK", data)
