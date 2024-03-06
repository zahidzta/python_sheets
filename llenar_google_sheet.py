import psycopg2
import gspread

#conexión con la hoja de calculo
gc = gspread.service_account(filename='river-tiger-413401-45dae3e36242.json')
sheet = gc.open("python")
wks = sheet.worksheet("Hoja 1")

#conexión con la base de datos
try:
    connection = psycopg2.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "prueba",
        port = "5432"
    )
    print("Conexión exitosa")
except Exception as e:
    print(e)

#crea la cabecera de la tabla
def crear_cabecera():
    letra = 65
    #información de la base de datos
    cursor = connection.cursor()
    try:
        #consulta para obtener el nombre de las columnas
        cursor.execute("select column_name from information_schema.columns where table_name = 'usuarios'")
        rows = cursor.fetchall()
        #ciclo para colocar la cabecera
        for row in rows:
            cod_col = str(chr(letra)) + "1"
            wks.update([row], range_name=cod_col)
            letra += 1
    except Exception as e:
        print(e)
        

def llenar_hoja():
    cursor = connection.cursor()
    try:
        #consulta para seleccionar todos los registros de la tabla
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        #ciclo para agregar los registros
        for row in rows:
            wks.append_row(row)
    except Exception as e:
        print(e)



#Se necesita encontrar una manera de poder subir mas elementos a la hoja de calculo 
#Limitación para subir cierta cantidad de elementos por minuto
#{'code': 429, 'message': "Quota exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:675429720490'.", 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'RATE_LIMIT_EXCEEDED', 'domain': 'googleapis.com', 'metadata': {'quota_location': 'global', 'service': 'sheets.googleapis.com', 'quota_limit_value': '60', 'quota_limit': 'WriteRequestsPerMinutePerUser', 'consumer': 'projects/675429720490', 'quota_metric': 'sheets.googleapis.com/write_requests'}}, {'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Request a higher quota limit.', 'url': 'https://cloud.google.com/docs/quota#requesting_higher_quota'}]}]}
crear_cabecera()
llenar_hoja()