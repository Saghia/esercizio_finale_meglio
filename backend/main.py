#mi import fastapi per creare il backend in python
from fastapi import FastAPI, HTTPException
#per richieste standardizzate
from pydantic import BaseModel
#per connessione
import mysql.connector
#per evitare errori di CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#sempre per cors
# Middleware per gestire le intestazioni CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#file di configurazione per connessione
config = {
    "host" : "127.0.0.1", #indirizzo locale
    "port" : "3306", #standard
    "user" : "root", #standard
    "database" : "ristorante" #nome database
}

class check_tavolo(BaseModel):
    data: str
    ora: str
    

#rotta check tavoli
@app.post("/api/check_tavolo")
def check_tavolo(check_tavolo:check_tavolo):
    #classica connessione al database
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    #esecuzione query
    cursor.execute("SELECT * FROM tavoli WHERE data=%s AND ora=%s" , (check_tavolo.data, check_tavolo.ora))
    #fetchall restituisce una lista degli utenti trovati
    tavoli = cursor.fetchall()
    print(tavoli)
    #se la lista di risultati non esiste
    if not tavoli:
        raise HTTPException(status_code=200, detail="Tavolo Libero")
    #se la lista esiste
    else : 
        # 401 -> unauthorized -> per logica
        raise HTTPException(status_code=401, detail="Tavolo Occupato")

    
class prenota_tavolo(BaseModel):
    data: str
    ora: str
    numero_persone: int
    
    
#la rotta di prenotazione tavoli
@app.post("/api/prenota")
def registrazione(prenota_tavolo : prenota_tavolo):
    #connetto base base
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor()
    #execute
    cursor.execute("INSERT INTO tavoli (data, ora, numero_persone) VALUES (%s,%s,%s)" 
                   , (prenota_tavolo.data, prenota_tavolo.ora, prenota_tavolo.numero_persone))
    conn.commit()
    conn.close()
    raise HTTPException(status_code=201, detail="Tavolo Prenotato")

