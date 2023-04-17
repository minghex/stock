from handlers.base import BaseHandler

# import model.pcr as pcr

class PCRHandler(BaseHandler):
    def get(self):
        # df = pcr.OPTION_SZ50_LIST_HANDLER()
        # print(df)
        print("call pcrhandler")
        self.write("call pcr_handler")