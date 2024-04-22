from fastapi import FastAPI
import requests
from datetime import datetime
from dateutil import parser
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

id = os.environ.get('ID_PLAZA')
url = f'https://alquilatucancha.com/api/v3/availability/sportclubs/{id}?date='
id_cancha = '3891'
id_cancha61 = '3892'
id_cancha62 = '3893'

class Choice(BaseModel):
    hour: str
    
class Stadium(BaseModel):
    name: str
    choices: List[Choice] = []
    
    def add_choice(self, choice: Choice):
        self.choices.append(choice)

class Slots(BaseModel):
    stadiums: List[Stadium] = []
    
    def add_stadium(self, stadium: Stadium):
        self.stadiums.append(stadium)

@app.get("/health")
def read_root():
    return {"Hello": "World Tom"}

@app.get("/cancha", response_model=Slots)
def chat_openai(day: str):
    slots = Slots()
    response = requests.get(url+day)
    if response.status_code == 200:
    
        date_obj = datetime.strptime(day, "%Y-%m-%d")
        
        date_with_time = date_obj.replace(hour=18, minute=0, second=0)
        
        match_time = date_with_time.isoformat() + "-03:00"
        
        dt_comparacion = parser.parse(match_time)
    
        content = response.json()
        if 'available_courts' in content:
            for x in content['available_courts']:
                if x['id'] == id_cancha:
                    print(x)
                    if 'available_slots' in x:
                        stadium = Stadium(name="F5")
                        for a in x['available_slots']:
                            dt_actual = parser.parse(a['start'])
                            if dt_actual >= dt_comparacion:
                                print(a['start'])
                                stadium.add_choice(Choice(hour=a['start']))
                        print(stadium)
                        slots.add_stadium(stadium)
                elif x['id'] == id_cancha61:
                    if 'available_slots' in x:
                        stadium = Stadium(name="F6 1")
                        for a in x['available_slots']:
                            dt_actual = parser.parse(a['start'])
                            if dt_actual >= dt_comparacion:
                                stadium.add_choice(Choice(hour=a['start']))
                        slots.add_stadium(stadium)
                elif x['id'] == id_cancha62:
                    if 'available_slots' in x:
                        stadium = Stadium(name="F6 2")
                        for a in x['available_slots']:
                            dt_actual = parser.parse(a['start'])
                            if dt_actual >= dt_comparacion:
                                stadium.add_choice(Choice(hour=a['start']))
                        slots.add_stadium(stadium)
    else:
        print("Error:", response.status_code)
    
    return slots