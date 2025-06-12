#!/usr/bin/env  python3
# -- coding: utf-8 --
import json
import tkinter as tk
import os
import requests
import time
from datetime import datetime
from supabase import create_client, Client

url = "https://xrsgaczmlkoprohaovjz.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhyc2dhY3ptbGtvcHJvaGFvdmp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5NjA1NTgsImV4cCI6MjA2NDUzNjU1OH0.VDJxCEn-qHW4ac1W6nkNkEaCSpeFM-CgFVS4NfTa0lE"

supabase: Client = create_client(url, key)


def es_color_oscuro(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    luminancia = (0.299 * r + 0.587 * g + 0.114 * b)
    return luminancia < 128

colores_por_tipo = {
     "PLA": {
        "APPLEGREEN": "#8DB600", "ARMYGREEN": "#4B5320", "BLACK": "#000000", "BLUE": "#0000FF",
        "BROWN": "#8B4513", "COLORCHANGE": "#808080", "CRYSTAL": "#CCE5FF", "FLUORESCENTGREEN": "#39FF14",
        "FLUORESCENTORANGE": "#FF8000", "FLUORESCENTYELLOW": "#FFFF00", "FUCHSIA": "#FF00FF",
        "GLITTERARMYGREEN": "#556B2F", "GLITTERBLACK": "#222222", "GLITTERBLUE": "#4682B4",
        "GLITTERGOLD": "#FFD700", "GLITTERRED": "#FF6347", "GLITTERSILVER": "#C0C0C0",
        "GOLD": "#FFD700", "LIGHTBLUE": "#ADD8E6", "LIGHTBROWN": "#A0522D", "LIGHTPINK": "#FFB6C1",
        "MUSTARD": "#FFDB58", "NAFTASUPER": "#FA8072", "ORANGE": "#FFA500", "PASTELBLUE": "#AEC6CF",
        "PASTELCREAM": "#FFFDD0", "PASTELGREEN": "#77DD77", "PASTELPINK": "#FFD1DC",
        "PASTELVIOLET": "#CBAACB", "PINK": "#FFC0CB", "RED": "#FF0000", "SILVER": "#C0C0C0",
        "ULTRAWHITE": "#FFFFFF", "VIOLET": "#8A2BE2", "WHITE": "#F8F8FF", "YELLOW": "#FFFF00",
        "CAPIBARA": "#A68F6A", "FIREFLY": "#FF4500", "MIXSURTIDO": "#FFDB58", 
    },
    "SILK": {
        "SALUMINUM":"#4682B4","SBLUE": "#0000FF", "SFUCHSIA": "#FF00FF", "SGOLD": "#FFD700", "SGRAPHITE": "#4B4B4B",
        "SGREEN": "#228B22", "SPEACH": "#FFDAB9", "SPURPLE": "#800080", "SRED": "#FF0000",
        "SROSEGOLD": "#B76E79", "SSAND": "#C2B280", "SORANGEFLUOR" : "#FF8000", "SGREENFLUOR" : "#556B2F", "SYELLOWFLUOR" : "#FFFF00", "STRICOLORGREENPURPLEBLUE" : "#AEC6CF",
        "STRICOLORREDGOLDBLUE" : "#FFDB58", "STRICOLORGOLDPURPLEBLUE": "#FFD700",
        "STRICOLORREDORANGEGOLD": "#FF6347", "SCOLORCHANGE": "#A68F6A", "STRICOLORGREENPURPLEGOLD": "#0000FF","TRICOLORBLUEYELLOWFGREEN": "#4B4B4B", "TRICOLORGREENGOLDFUCHSIA": "#AEC6CF" 
    },
    "PETG": {
        "PAPPLEGREEN": "#8DB600", "PBLACK": "#000000", "PCRYSTAL": "#CCE5FF", "PRED": "#FF0000",
        "PVIOLET": "#8A2BE2", "PWHITE": "#F8F8FF", "PYELLOW": "#FFFF00", "PBLUE": "#0000FF", "PCOLORCHANGE" : "#808080",
    },
    "ABS": {
        "ABSBLACK": "#000000", "ABSWHITE": "#FFFFFF"
    },
    "ASA": {
        "ASABLACK": "#111111", "ASAWHITE": "#FFFFFF"
    }
    ,
    "FC": {
        "FBLACK": "#111111", "FSILVER": "#C0C0C0"
    }
}

def obtener_fecha_actual():
    # dd/mm/YYYY
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def enviar_log_a_google_form(datos):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSeJOIF9dChWZSWWlH5YK9YXT504_yIwaXDELyr7EFOBNDNRjA/formResponse"

    payload = {
        "entry.1411632158": datos["fecha"],
        "entry.1636210408": datos["tipo"],
        "entry.1036328496": datos["color"],
        "entry.2004314848": datos["id_filamento"],
        "entry.474366348":  datos["id_numero"],
        "entry.986741256":  datos["codigo_barra"],
        "entry.1876513930": datos["id_maquina"]
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Log enviado a Google Form con éxito.")
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al enviar a Google Form: {e}")

def imprimir_codigo_epico(id_numero, tipo, color, id_filamento):
    numero_formateado = f"{id_numero:010d}"
    fecha = datetime.now().strftime("%d/%m/%Y")

    contenido_barcode = f"{ID_MAQUINA}-{tipo}-{id_filamento}-{numero_formateado}"

    zpl = f"""
^XA
^LH0,0
^PW400

^FO20,200
^A0N,20,20
^FD      Codigo del producto: "{id_numero:010d}"^FS

^FO30,300
^A0N,30,30
^FDFecha: {fecha}^FS


^FO60,60^BY0.5,2,150
^BCN,100,Y,N,N
^FD{contenido_barcode}^FS

^FO30,320
^A0N,30,30
^FD{contenido_barcode}^FS

^XZ
"""
    ruta_temp = f"/tmp/etiqueta_epica_{numero_formateado}.prn"
    with open(ruta_temp, "w") as f:
        f.write(zpl)

    os.system(f"lp -d Zebra {ruta_temp}")

def imprimir_etiqueta(nombre_archivo):
    ruta_original = f"/home/gst3d/etiquetas/{nombre_archivo}.prn"
    ruta_temp     = f"/tmp/{nombre_archivo}_con_fecha.prn"
    fecha = obtener_fecha_actual()

   
    with open(ruta_original, 'r') as f:
        zpl = f.read()

 
    if "^XZ" in zpl:
        zpl_body, _ = zpl.rsplit("^XZ", 1)
    else:
        zpl_body = zpl

  
    overlay = f"""
    ^FO60,205
    ^A0N,30,30
    ^FDFecha: {fecha}^FS
    """

    zpl_final = zpl_body + overlay + "\n^XZ"

   
    with open(ruta_temp, 'w') as f:
        f.write(zpl_final)

    os.system(f"lp -d Zebra {ruta_temp}")

import re

def actualizar_botones(tipo):
    for w in frame_botones.winfo_children():
        w.destroy()

    colores = colores_por_tipo.get(tipo, {})
    cols = 6

    for idx, (etiqueta, color_hex) in enumerate(colores.items()):
        r, c = divmod(idx, cols)

        fg = "white" if es_color_oscuro(color_hex) else "black"

        # Empezamos con la etiqueta original
        etiqueta_mostrar = etiqueta

        # Reemplazos generales
        etiqueta_mostrar = (etiqueta_mostrar
            .replace("STRICOLORGREENPURPLEBLUE", "TRI- GREEN PURPLE BLUE")
            .replace("STRICOLORREDGOLDBLUE", "TRI- RED GOLD BLUE")
            .replace("STRICOLORGOLDPURPLEBLUE", "TRI- GOLD PURPLE BLUE")
            .replace("STRICOLORREDORANGEGOLD", "TRI- RED ORANGE GOLD")
            .replace("STRICOLOR", "TRI-")
            .replace("FLUORESCENT", "FLUO-")
            .replace("GLITTER", "GLIT-")
            .replace("COLORCHANGE", "COLOR-CHANGE")
        )

        # Si es tipo PETG, le sacamos la "P" del principio si existe
        if tipo == "PETG" and etiqueta_mostrar.startswith("P"):
            etiqueta_mostrar = etiqueta_mostrar[1:]

        # Si empieza con "SILK", le agregamos un guion
        if etiqueta_mostrar.startswith("SILK"):
            etiqueta_mostrar = etiqueta_mostrar.replace("SILK", "SILK-", 1)

        # Agregamos espacio entre mayúsculas si viene una después de una minúscula
        etiqueta_mostrar = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", etiqueta_mostrar)

        btn = tk.Button(frame_botones,
                        text=etiqueta,
                        bg=color_hex, fg=fg,
                        width=15, height=4,
                        wraplength=100,
                        command=lambda e=etiqueta, t=tipo: imprimir_y_guardar_etiqueta(
                            e,
                            t,
                            e,
                            "FILAMENT"
                        )
                    )

        btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

    for i in range(cols):
        frame_botones.columnconfigure(i, weight=1)

from datetime import datetime

def subir_etiqueta_supabase(tipo, color, id_filamento, id_numero):
    fecha = datetime.now().isoformat()
    data = {
        "fecha": fecha,
        "tipo": tipo,
        "color": color,
        "id_filamento": id_filamento,
        "id_numero": f"{id_numero:08d}",
    }
    response = supabase.table("etiquetas_filamento").insert(data).execute()
    if response.status_code == 201:
        print("Etiqueta subida con éxito a Supabase")
    else:
        print("Error al subir etiqueta:", response.data)
ARCHIVO_CONTADOR = "contador_id_numero.txt"

def leer_contador():
    import os
    if os.path.exists(ARCHIVO_CONTADOR):
        with open(ARCHIVO_CONTADOR, "r") as f:
            try:
                return int(f.read())
            except:
                return 1
    else:
        return 1

def guardar_contador(numero):
    with open(ARCHIVO_CONTADOR, "w") as f:
        f.write(str(numero))

ID_MAQUINA = "01"

def imprimir_y_guardar_etiqueta(nombre_archivo, tipo, color, id_filamento):
    id_numero = leer_contador()

    imprimir_etiqueta(nombre_archivo)
    imprimir_codigo_epico(id_numero, tipo, color, id_filamento)
        
    numero_formateado = f"{id_numero:010d}"
    contenido_barcode = f"{ID_MAQUINA}-{tipo}-{id_filamento}-{numero_formateado}"

    datos = {
        "fecha": datetime.now().isoformat(),
        "tipo": tipo,
        "color": color,
        "id_filamento": id_filamento,
        "id_numero": numero_formateado,
        "codigo_barra": contenido_barcode,
        "id_maquina": ID_MAQUINA
    }


    guardar_local(datos)
    guardar_contador(id_numero + 1)

    print(f"Etiqueta #{id_numero} impresa y guardada localmente")

    if hay_conexion():
        enviar_log_a_google_form(datos)
        threading.Thread(target=sincronizar_datos_locales, daemon=True).start()




# Conexion wifi chequeo y actualizacion de datos
def hay_conexion():
    try:
        requests.get('https://www.google.com', timeout=3)
        return True
    except:
        return False

def guardar_local(datos):
    try:
        with open("datos_locales.json", "a") as f:
            json.dump(datos, f)
            f.write("\n")
    except Exception as e:
        print(f"Error al guardar localmente: {e}")

def sincronizar_datos_locales():
    print("🔁 Intentando sincronizar datos locales...")

    if not os.path.exists("datos_locales.json"):
        print("⚠️ Archivo 'datos_locales.json' no existe.")
        return

    if not hay_conexion():
        print("❌ No hay conexión a internet.")
        return

    try:
        with open("datos_locales.json", "r") as f:
            lineas = f.readlines()
            if not lineas:
                print("⚠️ El archivo existe pero está vacío.")
                return

            exitos = 0
            errores = 0

            for idx, linea in enumerate(lineas):
                print(f"📄 Línea {idx + 1} cruda: {linea.strip()}")

                try:
                    datos = json.loads(linea)
                    print(f"📦 Datos cargados: {datos}")
                    
                    response = supabase.table('etiquetas_filamento').insert(datos).execute()
                    print("🧾 Respuesta de Supabase:", response)

                    if hasattr(response, 'status_code') and response.status_code == 201:
                        print(f"✅ Línea {idx + 1} subida correctamente.")
                        exitos += 1
                        enviar_log_a_google_form(datos)
                    else:
                        print(f"❌ Línea {idx + 1} falló: {getattr(response, 'data', 'Sin detalles')}")
                        errores += 1

                except json.JSONDecodeError as e:
                    print(f"💥 Error de JSON en línea {idx + 1}: {e}")
                    errores += 1
                except Exception as e:
                    print(f"💣 Error inesperado al subir línea {idx + 1}: {e}")
                    errores += 1
        if exitos > 0:
            mensaje = f"📦 Raspberry {ID_MAQUINA}:\n✅ {exitos} etiquetas sincronizadas.\n"
        if errores > 0:
            mensaje += f"❌ {errores} con errores.\n"
        mensaje += "📡 Fin de sincronización."
        enviar_telegram(mensaje)

        if errores == 0 and exitos > 0:
            os.remove("datos_locales.json")
            print("🗑️ Todos los datos subidos. Archivo local eliminado.")
        elif errores > 0:
            print(f"⚠️ {errores} errores al sincronizar. Archivo no se borra.")
        else:
            print("🤔 No se subió ningún dato.")

    except Exception as e:
        print(f"💣 Error general durante la sincronización: {e}")
#Telegram
def enviar_telegram(mensaje):
    bot_token = "7974540435:AAEcjxJTplsM--ZgKKXZpsG7ZCg_oWCmqeo"
    chat_id = "-4919139591"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensaje
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Error al enviar mensaje Telegram: {e}")   
# INTERFAZ TK 
root = tk.Tk()
root.title("Impresion de etiquetas")
root.update()
root.attributes('-fullscreen', True)
root.overrideredirect(True)
root.configure(bg="#2e2e2e")
    
tipo_var = tk.StringVar(value="PLA")
tk.OptionMenu(root, tipo_var, *colores_por_tipo.keys(), command=actualizar_botones).pack(pady=10)
btn_sync = tk.Button(root, text="🔁 Sincronizar ahora", font=("Arial", 14),
                     bg="#444", fg="white", activebackground="#666",
                     command=lambda: threading.Thread(target=sincronizar_datos_locales, daemon=True).start())
btn_sync.pack(pady=5)
canvas = tk.Canvas(root)

from tkinter import ttk
sb = tk.Scrollbar(root, orient="vertical", command=canvas.yview, width=20)
style = ttk.Style()
style.theme_use('default')
style.configure("Vertical.TScrollbar", gripcount=0,
                background="#555", darkcolor="#444", lightcolor="#666",
                troughcolor="black", bordercolor="black", arrowcolor="white",
                width=30)
frame_botones = tk.Frame(canvas)
frame_botones.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0), window=frame_botones, anchor="nw")
canvas.configure(yscrollcommand=sb.set)
canvas.pack(side="left",  fill="both", expand=True)
sb.pack(       side="right", fill="y"      )

actualizar_botones("PLA")

import threading
root.mainloop() 