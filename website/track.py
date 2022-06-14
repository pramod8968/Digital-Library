import datetime
from .models import Stats
from . import db


#User Visit to a book tracking
def uvt(book_id):
    week_no = datetime.date.today().isocalendar()[1]
    year = datetime.date.today().year
    dstamp = str(week_no)+"-"+str(year)
    week = Stats.query.filter_by(book_id= book_id, week_stamp=dstamp).first()
    if week:
        week.unique_visits=week.unique_visits+1
        db.session.commit()
        print(week.unique_visits)
    else:
        stats = Stats(book_id=book_id,week_stamp = dstamp, unique_visits=1)
        db.session.add(stats)
        db.session.commit()

def issue_track(book_id):
    week_no = datetime.date.today().isocalendar()[1]
    year = datetime.date.today().year
    dstamp = str(week_no)+"-"+str(year)
    week = Stats.query.filter_by(book_id= book_id, week_stamp=dstamp).first()
    if week:
        week.number_of_issues=week.number_of_issues+1
        db.session.commit()
        print(week.number_of_issues)
    else:
        stats = Stats(book_id=book_id,week_stamp = dstamp, number_of_issues=1)
        db.session.add(stats)
        db.session.commit()
#User notify me clicks count

def notify_click_track(book_id):
    week_no = datetime.date.today().isocalendar()[1]
    year = datetime.date.today().year
    dstamp = str(week_no)+"-"+str(year)
    week = Stats.query.filter_by(book_id= book_id, week_stamp=dstamp).first()
    if week:
        week.number_notify_me=week.number_notify_me+1
        db.session.commit()
        print(week.number_notify_me)
    else:
        stats = Stats(book_id=book_id,week_stamp = dstamp, number_notify_me=1)
        db.session.add(stats)
        db.session.commit()