import gspread

def acutalizar_cabecera(wks, cabeceras):
    cant_cols = wks.col_count
    letra = 65
    col = 0

    while col < cant_cols:
        #Genera codigo de la columna
        cod_col = str(chr(letra)) + "1"
        #Para agregar o actualizar un valor de la cabecera
        if col < len(cabeceras) and cabeceras[col] != wks.acell(cod_col).value:
            wks.update([[cabeceras[col]]], range_name=cod_col)
        #Para borrar cualquier valor que no se encuentre en la cabecera
        elif wks.acell(cod_col).value != "" and col >= len(cabeceras):
            wks.update([[""]], range_name=cod_col)
        letra += 1
        col += 1

gc = gspread.service_account(filename='river-tiger-413401-45dae3e36242.json')
sheet = gc.open("python")
wks = sheet.worksheet("Hoja 1")


cabeceras = ['Nombre', 'Primer apellido', 'Segundo apellido']

print("Opciones")
print("1. Actualizar cabecera")
print("2. Agregar dato")
opcion = int(input("Opcion: "))
datos = []
if opcion == 1:
    print("Esto puede tardar unos segundos")
    acutalizar_cabecera(wks, cabeceras)
    print("Listo")
else:
    for cabecera in cabeceras:
        datos.append(input(f"Ingresa {cabecera}: "))
    wks.append_row(datos) 

