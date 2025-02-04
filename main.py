from fastapi import FastAPI, Request
import json
import os
from datetime import datetime

app = FastAPI()

# Nombre del archivo donde se guardarán los eventos
EVENT_LOG_FILE = "event_log.json"

@app.post("/events")
async def receive_event(request: Request):
    try:
        # Obtener datos del evento recibido
        event_data = await request.json()
        print("Evento recibido:", event_data)

        # Cargar eventos previos o iniciar una lista nueva
        if os.path.exists(EVENT_LOG_FILE):
            with open(EVENT_LOG_FILE, "r", encoding="utf-8") as file:
                try:
                    events = json.load(file)
                except json.JSONDecodeError:
                    events = []
        else:
            events = []

        # Agregar nuevo evento con timestamp
        events.append({
            "timestamp": datetime.now(datetime.timezone.utc).isoformat(),
            "event": event_data
        })

        # Guardar eventos en el archivo
        with open(EVENT_LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(events, file, indent=4, ensure_ascii=False)

        # Responder con HTTP 200 y el formato esperado
        return {
            "ResponseStatus": {
                "statusCode": 1,
                "statusString": "OK"
            }
        }
    
    except Exception as e:
        print("Error procesando el evento:", str(e))
        return {
            "ResponseStatus": {
                "statusCode": 5,
                "statusString": "Internal Server Error"
            }
        }

