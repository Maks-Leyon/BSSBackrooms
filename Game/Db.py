from peewee import *

db = SqliteDatabase('game_data.db')

class BaseModel(Model):
    '''Klasa bazowa dla wszystkich modeli w bazie danych.'''
    class Meta:
        database = db

class PlayerInfo(BaseModel):
    '''Klasa ta reprezentuje informacje o graczu.'''
    x = FloatField()
    y = FloatField()
    rotationSpeed = FloatField()
    angle = FloatField()
    stamina = FloatField()
    hp = IntegerField()

class EnemyInfo(BaseModel):
    '''Klasa ta reprezentuje informacje o przeciwniku.'''
    x = FloatField()
    y = FloatField()
    stamina = FloatField()
    start_chase = BooleanField()

class GameInfo(BaseModel):
    '''Klasa ta przechowuje informacje o stanie gry.'''
    elapsed_time = FloatField()
    level = IntegerField()
    note_count = IntegerField()

class NoteModel(BaseModel):
    '''Klasa ta reprezentuje notatkę w grze.'''
    index = IntegerField()
    collected = BooleanField()

class PickupModel(BaseModel):
    '''Klasa ta reprezentuje przedmiot do zebrania w grze.'''
    index = IntegerField()
    collected = BooleanField()

class WinInfo(BaseModel):
    '''Klasa ta przechowuje informacje o zwycięstwie w grze.'''
    time = FloatField()
    nick = CharField()

db.connect()
db.create_tables([GameInfo, PlayerInfo, EnemyInfo, NoteModel, PickupModel, WinInfo])
