from handlers.foo import *

url_patterns = [
    (r"/",MainHandler),
    (r"/login",LoginHandler),
    (r"/insert",InsertHandler),
    (r"/delete/(\d+)",DeleteHandler),
    (r"/change/(\d+)",ChangeHandler),
    (r"/changecustomer/(\d+)",ChangeCustomerHandler),
    (r"/customer_detail/(\d+)",CustomerdetailHandlder),
    (r"/logout",LogoutHandler),
    (r"/getcookie",GetcookieHandler),
    (r"/detail/(\d+)",DetailHandler),
    (r"/newinsert",NewInsertHandler),
    (r"/customer",CustomerHandler),
    (r"/insert_customer",InsertcustomerHandler),
    (r"/customer_delete/(\d+)",CustomerdeleteHandler),
    (r"/searchdate",SearchDateHandler)

]
