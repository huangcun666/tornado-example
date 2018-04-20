# encoding=utf8  
from handlers.base import BaseHandler
import logging
import json
import tornado.web
import urllib2
import tornado.httpclient
import sys,re
import urllib
reload(sys)  
sys.setdefaultencoding('utf8')   

logger = logging.getLogger('boilerplate.' + __name__)

class DetailHandler(BaseHandler):
    def get(self,id):
        db=self.application.db
        customers=db.query("select * from customer where id=%s",int(id))
        customer=customers[0]
        self.render('show_table.html',customer=customer)

class GetcookieHandler(BaseHandler):
    def get(self):
        client=tornado.httpclient.HTTPClient()
        response=client.fetch("http://192.168.2.168:9000/capi?tag=project&id=231")
        customer=json.loads(response.body)
        self.write(customer['customer']['craeted_at'])

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username=self.get_argument('exampleInputEmail1')
        password=self.get_argument('exampleInputPassword1')
        client=tornado.httpclient.HTTPClient()
        response=client.fetch("http://192.168.2.168:9000/oapi?"+\
        urllib.urlencode({"tag":'auth','username':username,'password':password}))
        user=json.loads(response.body)
        if user['uid'] ==0:
            self.render('login.html',error=user['error'])
        self.set_secure_cookie('username',user['username'])
        self.set_secure_cookie('role',user['role'])
        self.set_secure_cookie('uid',str(user['uid']))
        self.set_secure_cookie('log_user',username)
        self.redirect('/')

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db=self.application.db
        indents=db.query("select * from customer order by cus_id asc")
        self.render('main.html',indents=indents)

class CustomerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db=self.application.db
        customers=db.query("select * from customer_manage order by customer_id asc")
        self.render('customer.html',customers=customers)

class CustomerForm(object):
    def __init__(self):
        self.customer_id="(^\d+$)"

    def check_valid(self,request):
        flag=True
        form_dict=self.__dict__
        allerror_message={}
        error_message={} 
        for key,regular in form_dict.items():
            post_value=request.get_argument(key)
            ret=re.match(regular,post_value)
            if not ret:
                flag=False
        return flag

class InsertcustomerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('insertcustomer.html')
    
    @tornado.web.authenticated
    def post(self):
        cusform=CustomerForm()
        cus=cusform.check_valid(self)
        if not cus:
            self.redirect('/insert_customer')
        db=self.application.db
        customer_id=self.get_argument('customer_id')
        customers=db.query('select * from customer_manage where customer_id=%s',customer_id)
        if len(customers)!=0:
            self.render('insertcustomer.html',error_id=customer_id)
        company=self.get_argument('company')
        linkman=self.get_argument('linkman')
        phone=self.get_argument('phone')
        yewu_content=self.get_argument('yewu_content')
        address_style=self.get_argument('address_style')
        start_hetong=self.get_argument('start_hetong') or None
        end_hetong=self.get_argument('end_hetong') or None
        date_chengli=self.get_argument('date_chengli') or None
        date_zhizhao=self.get_argument('date_zhizhao') or None
        date_address=self.get_argument('date_address') or None
        kf_name=self.get_argument('kf_name')
        sale_name=self.get_argument('sale_name')
        zhuanshang=self.get_argument('zhuanshang')
        kuaiji=self.get_argument('kuaiji')
        address_gongying=self.get_argument('address_gongying')
        if start_hetong!=None:
            start_hetong=re.sub('/','-',start_hetong,2)
        if end_hetong!=None:
            end_hetong=re.sub('/','-',end_hetong,2)
        if date_chengli!=None:
            date_chengli=re.sub('/','-',date_chengli,2)
        if date_zhizhao!=None:
            date_zhizhao=re.sub('/','-',date_zhizhao,2)
        if date_address!=None:
            date_address=re.sub('/','-',date_address,2)
        db.execute('insert into customer_manage('
            'customer_id,company,linkman,phone,yewu_content,address_style,start_hetong,'
            'end_hetong,date_chengli,date_zhizhao,date_address,kf_name,sale_name,'
            'zhuanshang,kuaiji,address_gongying) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            customer_id,company,linkman,phone,yewu_content,address_style,start_hetong,
            end_hetong,date_chengli,date_zhizhao,date_address,kf_name,sale_name,zhuanshang,kuaiji,address_gongying)
        self.redirect('/customer')

class ChangeCustomerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        db=self.application.db
        customers=db.query('select * from customer_manage where id=%s',int(id))
        customer=customers[0]
        self.render('insertcustomer.html',customer=customer)
    
    @tornado.web.authenticated
    def post(self,id):
        cusform=CustomerForm()
        cus=cusform.check_valid(self)
        if not cus:
            self.redirect('/insert_customer')
        db=self.application.db
        customer=db.query('select * from customer_manage where id=%s',int(id))
        customer=customer[0]
        customer_id=self.get_argument('customer_id')
        if int(customer_id)!=customer.customer_id:
            customers=db.query('select * from customer_manage where customer_id=%s',int(customer_id))
            if len(customers)!=0:
                self.render('insertcustomer.html',customer=customer,error_id=customer_id)
            company=self.get_argument('company')
            linkman=self.get_argument('linkman')
            phone=self.get_argument('phone')
            yewu_content=self.get_argument('yewu_content')
            address_style=self.get_argument('address_style')
            start_hetong=self.get_argument('start_hetong') or None
            end_hetong=self.get_argument('end_hetong') or None
            date_chengli=self.get_argument('date_chengli') or None
            date_zhizhao=self.get_argument('date_zhizhao') or None
            date_address=self.get_argument('date_address') or None
            kf_name=self.get_argument('kf_name')
            sale_name=self.get_argument('sale_name')
            zhuanshang=self.get_argument('zhuanshang')
            kuaiji=self.get_argument('kuaiji')
            address_gongying=self.get_argument('address_gongying')
            if start_hetong!=None:
                start_hetong=re.sub('/','-',start_hetong,2)
            if end_hetong!=None:
                end_hetong=re.sub('/','-',end_hetong,2)
            if date_chengli!=None:
                date_chengli=re.sub('/','-',date_chengli,2)
            if date_zhizhao!=None:
                date_zhizhao=re.sub('/','-',date_zhizhao,2)
            if date_address!=None:
                date_address=re.sub('/','-',date_address,2)
            db.execute('update  customer_manage set customer_id=%s,company=%s,'
                'linkman=%s,phone=%s,yewu_content=%s,address_style=%s,start_hetong=%s,'
                'end_hetong=%s,date_chengli=%s,date_zhizhao=%s,date_address=%s,kf_name=%s,sale_name=%s,'
                'zhuanshang=%s,kuaiji=%s,address_gongying=%s where id=%s',
                int(customer_id),company,linkman,phone,yewu_content,address_style,start_hetong,
                end_hetong,date_chengli,date_zhizhao,date_address,kf_name,sale_name,zhuanshang,kuaiji,address_gongying,int(id))
            self.redirect('/customer')
        else:
            company=self.get_argument('company')
            linkman=self.get_argument('linkman')
            phone=self.get_argument('phone')
            yewu_content=self.get_argument('yewu_content')
            address_style=self.get_argument('address_style')
            start_hetong=self.get_argument('start_hetong') or None
            end_hetong=self.get_argument('end_hetong') or None
            date_chengli=self.get_argument('date_chengli') or None
            date_zhizhao=self.get_argument('date_zhizhao') or None
            date_address=self.get_argument('date_address') or None
            kf_name=self.get_argument('kf_name')
            sale_name=self.get_argument('sale_name')
            zhuanshang=self.get_argument('zhuanshang')
            kuaiji=self.get_argument('kuaiji')
            address_gongying=self.get_argument('address_gongying')
            if start_hetong!=None:
                start_hetong=re.sub('/','-',start_hetong,2)
            if end_hetong!=None:
                end_hetong=re.sub('/','-',end_hetong,2)
            if date_chengli!=None:
                date_chengli=re.sub('/','-',date_chengli,2)
            if date_zhizhao!=None:
                date_zhizhao=re.sub('/','-',date_zhizhao,2)
            if date_address!=None:
                date_address=re.sub('/','-',date_address,2)
            db.execute('update  customer_manage set customer_id=%s,company=%s,'
                'linkman=%s,phone=%s,yewu_content=%s,address_style=%s,start_hetong=%s,'
                'end_hetong=%s,date_chengli=%s,date_zhizhao=%s,date_address=%s,kf_name=%s,sale_name=%s,'
                'zhuanshang=%s,kuaiji=%s,address_gongying=%s where id=%s',
                int(customer_id),company,linkman,phone,yewu_content,address_style,start_hetong,
                end_hetong,date_chengli,date_zhizhao,date_address,kf_name,sale_name,zhuanshang,kuaiji,address_gongying,int(id))
            self.redirect('/customer')


class CustomerdetailHandlder(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        db=self.application.db
        customer=db.query('select * from customer_manage where id=%s',int(id))
        customer=customer[0]
        self.render('show_table1.html',customer=customer)
        
class SearchDateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db=self.application.db
        timedate=self.get_argument('select_date')
        start_time=self.get_argument('start_time')
        end_time=self.get_argument('end_time')
        customers=db.query('select * from customer_manage where date(%s) between %s and %s',timedate,start_time,end_time)


class CustomerdeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        db=self.application.db
        db.execute('delete from customer_manage where id=%s',int(id))


class NewInsertHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('insert.html')

class InsertHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        try:
            id=self.get_argument('insert')
            client=tornado.httpclient.HTTPClient()
            response=client.fetch("http://192.168.2.168:9000/capi?"+\
            urllib.urlencode({'tag':'project','id':id}))
            customer=json.loads(response.body)
            if customer['code']==0 and id!='':
                self.render('insert.html',err_id=id)
            self.render('insert.html',customer=customer['customer'])
        except:
            self.redirect('/newinsert')
           
        
    @tornado.web.authenticated
    def post(self):
        m=MainForm()
        if m.check_valid(self):
            db=self.application.db
            sale_name=self.get_argument('sale_name')
            craeted_at=self.get_argument('craeted_at')
            project_name=self.get_argument('project_name')
            all_income=self.get_argument('all_income') or None
            kf_name=self.get_argument('kf_name')
            customer_company=self.get_argument('customer_company')
            cus_id=self.get_argument('cus_id')
            customer_name=self.get_argument('customer_name')
            income_type=self.get_argument('income_type')
            income_name=self.get_argument('income_name')
            customers=db.query('select * from customer where cus_id=%s',int(cus_id))
            if len(customers)!=0:
                self.render('insert.html',err_id2=cus_id)
            if all_income!=None:
                all_income=float(all_income)
            db.execute("insert into customer(sale_name,craeted_at,project_name,all_income,kf_name,customer_company,cus_id,"
                            "customer_name,income_type,income_name)"
                            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",sale_name
                            ,craeted_at,project_name,all_income,kf_name,customer_company,cus_id,
                            customer_name,income_type,income_name)
            self.redirect('/')
        else:
            self.redirect('/newinsert')              
            
class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        db=self.application.db
        indents=db.query("select * from customer where id=%s",int(id))
        indent=indents[0]
        if not indent:
            return None
        db.execute('delete from customer where id=%s',int(id))

class ChangeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        db=self.application.db
        indents=db.query("select * from customer where id=%s",int(id))
        indent=indents[0]
        if not indent:
            return None
        self.render('change.html',indent=indent)

    @tornado.web.authenticated
    def post(self,id):
        m1=MainForm()
        db=self.application.db
        indents=db.query("select * from customer where id=%s",int(id))
        indent=indents[0]
        if m1.check_valid(self)==False:
            self.render('change.html',indent=indent)

        cus_id=self.get_argument('cus_id')
        if int(cus_id)!=int(indent.cus_id):
            customers=db.query('select * from customer where cus_id=%s',int(cus_id))
            if len(customers)!=0:
                self.render('change.html',indent=indent,error_id=customers[0].cus_id)
            else:
                sale_name=self.get_argument('sale_name')
                craeted_at=self.get_argument('craeted_at')
                project_name=self.get_argument('project_name')
                all_income=self.get_argument('all_income') or None
                kf_name=self.get_argument('kf_name')
                customer_company=self.get_argument('customer_company')
                customer_name=self.get_argument('customer_name')
                income_type=self.get_argument('income_type')
                income_name=self.get_argument('income_name')
                if all_income!=None:
                    all_income=float(all_income)
                db.execute("update customer set sale_name=%s,craeted_at=%s,project_name=%s,all_income=%s,kf_name=%s,"
                "customer_company=%s,cus_id=%s,customer_name=%s,income_type=%s,income_name=%s where id=%s",
                sale_name,craeted_at,project_name,all_income,kf_name,customer_company,cus_id,customer_name,income_type,income_name,int(id)
                )
                self.redirect("/")
        else:
            sale_name=self.get_argument('sale_name')
            craeted_at=self.get_argument('craeted_at')
            project_name=self.get_argument('project_name')
            all_income=self.get_argument('all_income') or None
            kf_name=self.get_argument('kf_name')
            customer_company=self.get_argument('customer_company')
            customer_name=self.get_argument('customer_name')
            income_type=self.get_argument('income_type')
            income_name=self.get_argument('income_name')
            if all_income!=None:
                all_income=float(all_income)
            db.execute("update customer set sale_name=%s,craeted_at=%s,project_name=%s,all_income=%s,kf_name=%s,"
            "customer_company=%s,cus_id=%s,customer_name=%s,income_type=%s,income_name=%s where id=%s",
            sale_name,craeted_at,project_name,all_income,kf_name,customer_company,cus_id,customer_name,income_type,income_name,int(id)
            )
            print('7')
            self.redirect("/")
  
class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('log_user')
        self.redirect('/')

class MainForm(object):
    def __init__(self):
        self.cus_id=r"^\d+$"
        self.craeted_at=r"^(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})$"
        self.all_income=r"^\d*\.*\d*$"


    def check_valid(self,request):
        flag=True
        form_dict=self.__dict__
        # allerror_message={'serice':'不能为空','company':'不能为空',
        #                 'money':'不能为空','receipt_account':'不能为空',
        #                 'cashier':'不能为空','sales_consultant':'不能为空',
        #                 'service_consultant':'不能为空'}
        error_message={} 
        for key,regular in form_dict.items():
            post_value=request.get_argument(key)
            ret=re.match(regular,post_value)
            if not ret:
                # error_message[key]=allerror_message[key]
                flag=False
        return flag

