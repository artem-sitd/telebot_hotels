import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase("db_history.db")


class BaseModel(pw.Model):
    class Meta:
        database = db


class History(BaseModel):
    user_id = pw.IntegerField()
    created_at = pw.DateField(default=datetime.now())
    hotels = pw.CharField(max_length=400)

    class Meta:
        db_table = "History"


History.create_table()
