import pandas as pd
from .models import Stats
from sqlalchemy import create_engine
import sqlalchemy
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from flask import current_app
from io import BytesIO
import base64

def demand_graph(book):
    img = BytesIO()
    stats = Stats.query.filter_by(book_id=book.id).all()
    df = pd.DataFrame(columns=['id','week_stamp','book_id','demand_time','dt','number_of_issues','number_notify_me','unique_visits','Demand','number_of_copies'])
    df1 = pd.DataFrame(columns=['name','age','water'])
    # df = pd.DataFrame(stats[0],columns=['id','week_stamp','book_id','demand_time','dt','number_of_issues','number_notify_me','unique_visits','demand','number_of_copies'])
    i = 0
    for stat in stats:
        df.loc[i] = [stat.id, stat.week_stamp, stat.book_id,stat.demand_time,stat.dt,stat.number_of_issues,stat.number_notify_me,stat.unique_visits,stat.demand,stat.number_of_copies] 
        i=i+1
    plot_df = df[['week_stamp','number_of_copies','Demand']]

    demand_mean = [np.mean(df.Demand)]*len(plot_df)
    demand_mean_value = plot_df['Demand'].rolling(window=12).mean()

    nc_mean_value = plot_df['number_of_copies'].rolling(window=12).mean()

    plt.plot(plot_df.Demand, label = "Demand")
    plt.plot(plot_df.number_of_copies, label = "Number of Copies")
    plt.plot(demand_mean_value, label = "Demand Mean Curve")
    plt.plot(nc_mean_value, label = "Available Copies Mean Curve")

    plt.legend()
    plt.show()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url
