from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # for add data to the db
import pandas as pd


engine = create_engine('mysql+pymysql://root:T1o2mmy3#@localhost/db1', echo = True)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

class Stocks(Base):
   __tablename__ = 'Stock'
   id = Column(Integer, primary_key=True)
   ticker = Column(String(16))
   current_price = Column(Float)
   open_price = Column(Float)
   close_price = Column(Float)
   purchase_num = Column(Integer)
   sell_num = Column(Integer)

def get_record():
   ticker_list = []
   current_price_list = []
   open_price_list = []
   close_price_list = []
   purchase_num_list = []
   sell_num_list = []

   result = session.query(Stocks).all()
   print('type of result: ', type(result))
   iterator = 0
   for row in result:
      if iterator > 5:
         break

      ticker_list.append(row.ticker)
      current_price_list.append(row.current_price)
      open_price_list.append(row.open_price)
      close_price_list.append(row.close_price)
      purchase_num_list.append(row.purchase_num)
      sell_num_list.append(row.sell_num)

      iterator += 1

   new_dict = {'stock name': ticker_list, 'current price': current_price_list, 'open price': open_price_list,
   'close price': close_price_list, 'purchase num': purchase_num_list, 'sell num': sell_num_list}
   df = pd.DataFrame(new_dict)
   return df

def create_record():
   Base.metadata.create_all(engine)

def add_record(input_id, input_ticker, input_current_price, input_open_price, input_close_price, input_purchase_num, input_sell_num):
   c1 = Stocks(id = input_id, ticker = input_ticker, current_price = input_current_price, open_price = input_open_price, close_price = input_close_price, purchase_num = input_purchase_num, sell_num = input_sell_num)
   session.add(c1)
   session.commit()

def del_record(del_id):
   session.query(Stocks).filter(Stocks.id==2).delete()
   session.commit()

def update_record():
   session.query(Stocks).filter(Stocks.id==2).update({Stocks.open_price:200}, synchronize_session = False)
   session.commit()


#add_record(1,3,128,120,140,20,0)
#del_record(1)
#update_record()
#get_record()




