import json
import requests

# Leer las variables del archivo de configuración
with open('config.json') as config_file:
    config = json.load(config_file)

USER = config['USER']
PASSWORD = config['PASSWORD']
INSTANCE = config['INSTANCE']
print(f"Se inicia el script de envio de IRs")

# Función para crear un ticket de tipo "Problema" en ServiceNow
def create_problem_ticket(artefacto, documentacion):
    url = f'https://{INSTANCE}.service-now.com/api/now/table/problem'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {
        "short_description": f"Nuevo artefacto: {artefacto}",
        "description": f"Documentación relacionada:\n{documentacion}"
    }
    response = requests.post(url, auth=(USER, PASSWORD), headers=headers, json=data)
    if response.status_code == 201:
        return response.json()['result']['sys_id']
    else:
        print("Error al crear el ticket de problema:", response.text)
        return None

# Suponiendo que tienes una lista de registros con id, artefacto y documentación
registros = [
    {"id": 1, "artefacto": "Artefacto 1", "documentacion": "Documentación para Artefacto 1"},
    {"id": 2, "artefacto": "Artefacto 2", "documentacion": "Documentación para Artefacto 2"},
    {"id": 3, "artefacto": "Artefacto 3", "documentacion": "Documentación para Artefacto 3"}
]

# Lista para mantener un registro de los tickets creados para cada registro
tickets_por_registro = []

# Crear un ticket de tipo "Problema" para cada registro
for registro in registros:
    artefacto = registro['artefacto']
    documentacion = registro['documentacion']
    ticket_id = create_problem_ticket(artefacto, documentacion)
    if ticket_id:
        print(f"Ticket de problema creado para el artefacto '{artefacto}' con ID: {ticket_id}")
        tickets_por_registro.append({"id_registro": registro['id'], "ticket_id": ticket_id})

# Imprimir la relación entre registros y tickets
print("Relación entre registros y tickets:")
for rel in tickets_por_registro:
    print(f"Registro ID: {rel['id_registro']} --> Ticket ID: {rel['ticket_id']}")