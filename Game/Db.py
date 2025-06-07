from peewee import *


#BAZA DANYCH - MEGA EZ, MODELE JAKO KLASY, PO PROSTU ZAPISUJE DANE
db = SqliteDatabase('game_data.db')

class BaseModel(Model):
    class Meta:
        database = db

class PlayerInfo(BaseModel):
    x = FloatField()
    y = FloatField()
    rotationSpeed = FloatField()
    angle = FloatField()
    stamina = FloatField()
    hp = IntegerField()

class EnemyInfo(BaseModel):
    x = FloatField()
    y = FloatField()
    stamina = FloatField()
    start_chase = BooleanField()

class GameInfo(BaseModel):
    elapsed_time = FloatField()
    level = IntegerField()
    note_count = IntegerField()

class NoteModel(BaseModel):
    index = IntegerField()
    collected = BooleanField()

class PickupModel(BaseModel):
    index = IntegerField()
    collected = BooleanField()

class WinInfo(BaseModel):
    time = FloatField()
    nick = CharField()

db.connect()
db.create_tables([GameInfo, PlayerInfo, EnemyInfo, NoteModel, PickupModel, WinInfo])
