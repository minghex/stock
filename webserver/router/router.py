from controller.handler import * 
from controller.option.option_pcr import option_pcr_handler 
from controller.stock.stock_bond_margin import stock_pe_bond_Handler 
from controller.stock.stock_cxsl_xxtp import stock_csxl_xxtp_handler 
from controller.stock.stock_north import stock_north_net_flow

class backend_handler(BaseHandler):
    async def get(self):
        self.write_success_response("webserver backend")

routers = [
    (r'/', backend_handler),
    #期权PCR
    (r'/option_pcr', option_pcr_handler),
    #股债利差
    (r'/stock_pe_bond', stock_pe_bond_Handler),
    #持续缩量,向下突破
    (r'/stock/cxsl/xxtp',stock_csxl_xxtp_handler),
    #北向净流入
    (r'/stock/north/netflow', stock_north_net_flow)
]