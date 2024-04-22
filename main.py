from fastapi import FastAPI
import requests
from datetime import datetime
from dateutil import parser
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

id = os.environ.get("ID_PLAZA")
url = f'https://alquilatucancha.com/api/v3/availability/sportclubs/{id}?date='
id_cancha = os.environ.get("ID_CANCHA")

class Choice(BaseModel):
    hour: str

class Slots(BaseModel):
    choices: List[Choice] = []
    
    def add_choice(self, choice: Choice):
        self.choices.append(choice)

@app.get("/cancha", response_model=Slots)
def chat_openai(day: str):
    slots = Slots()
    response = requests.get(url+day)
    if response.status_code == 200:
    
        date_obj = datetime.strptime(day, "%Y-%m-%d")
        
        date_with_time = date_obj.replace(hour=18, minute=0, second=0)
        
        match_time = date_with_time.isoformat() + "-03:00"
        
        dt_comparacion = parser.parse(match_time)
    
        # Acceder al contenido de la respuesta
        content = response.json()
        if 'available_courts' in content:
            for x in content['available_courts']:
                if x['id'] == id_cancha:
                    if 'available_slots' in x:
                        for a in x['available_slots']:
                            dt_actual = parser.parse(a['start'])
                            if dt_actual >= dt_comparacion:
                                slots.add_choice(Choice(hour=a['start']))
    else:
        print("Error:", response.status_code)
        
    return slots