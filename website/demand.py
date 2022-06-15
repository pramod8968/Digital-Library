import pandas as pd
from .models import Stats
from sqlalchemy import create_engine
import sqlalchemy
import sqlite3
import pandas as pd

def demand_graph(book):
    stats = Stats.query.filter_by(book_id=book.id).all()
    df = pd.DataFrame(columns=['id','week_stamp','book_id','demand_time','dt','number_of_issues','number_notify_me','unique_visits','demand','number_of_copies'])
    df1 = pd.DataFrame(columns=['name','age','water'])
    print(df)
    # df = pd.DataFrame(stats[0],columns=['id','week_stamp','book_id','demand_time','dt','number_of_issues','number_notify_me','unique_visits','demand','number_of_copies'])
    i = 0
    for stat in stats:
        df.loc[i] = [stat.id, stat.week_stamp, stat.book_id,stat.demand_time,stat.dt,stat.number_of_issues,stat.number_notify_me,stat.unique_visits,stat.demand,stat.number_of_copies] 
        i=i+1
    print(df)
