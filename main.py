import streamlit as st
import pandas as pd
import requests
import json
import time
import random
import base64
from io import BytesIO
#streamlit run main.py
#pip freeze > requirements.txt

st.set_page_config(page_title="Enviador Masivo WhatsApp", layout="wide")

st.title("Enviador Masivo de Mensajes WhatsApp")

# Configuración de la API
with st.sidebar:
    st.header("Configuración")
    api_url = st.text_input("URL de Evolution API", "http://localhost:8080 o https://evolution-api.com")
    instance_name = st.text_input("Nombre de la instancia", "mi-instancia")
    api_key = st.text_input("API Key (si es necesaria)", type="password")
    delay = st.number_input("Retraso entre mensajes (segundos)", min_value=10, value=30)

# Carga de archivo
st.header("Paso 1: Cargar archivo con números")
file_info = st.info("Carga un archivo CSV o XLSX que contenga una columna con números de teléfono. El formato debe incluir el código de país (ej: 5215512345678)")
uploaded_file = st.file_uploader("Seleccionar archivo", type=["csv", "xlsx"])

# Vista previa y procesamiento de datos
numbers_df = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            numbers_df = pd.read_csv(uploaded_file)
        else:  # xlsx
            numbers_df = pd.read_excel(uploaded_file)
        
        st.success("Archivo cargado correctamente")
        
        # Selección de columna que contiene los números
        st.subheader("Selecciona la columna con los números telefónicos")
        phone_column = st.selectbox("Columna de números", numbers_df.columns.tolist())
        
        # Muestra una vista previa
        st.subheader("Vista previa de los datos")
        st.dataframe(numbers_df.head())
        
        # Información sobre cantidad de números
        total_numbers = len(numbers_df)
        st.info(f"Total de números detectados: {total_numbers}")
        
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")

# Configuración del mensaje
st.header("Paso 2: Componer mensaje")
message_text = st.text_area("Mensaje de texto", height=150)

# Opción para adjuntar imagen
st.subheader("Adjuntar imagen (opcional)")
image_file = st.file_uploader("Seleccionar imagen", type=["jpg", "jpeg", "png"])
caption = st.text_input("Pie de imagen (opcional)")

preview_col1, preview_col2 = st.columns(2)
with preview_col1:
    if message_text:
        st.subheader("Vista previa del mensaje:")
        st.markdown(f"```\n{message_text}\n```")

with preview_col2:
    if image_file is not None:
        st.subheader("Vista previa de la imagen:")
        st.image(image_file, width=300)
        if caption:
            st.caption(caption)

# Función para enviar mensajes
def send_messages():
    if not api_url or not instance_name:
        st.error("Por favor ingresa la URL de la API y el nombre de la instancia")
        return
    
    if not message_text and image_file is None:
        st.error("Por favor ingresa un mensaje o selecciona una imagen")
        return
    
    if numbers_df is None or phone_column not in numbers_df.columns:
        st.error("Por favor carga un archivo y selecciona la columna con los números")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Preparación de headers para la API
    headers = {
        "Content-Type": "application/json"
    }
    
    if api_key:
        headers["apikey"] = api_key
    
    # Contador de éxitos y errores
    successful = 0
    errors = 0
    
    # Lista para almacenar registros de envíos
    logs = []
    
    # Base64 encode de la imagen si existe
    image_base64 = None
    if image_file is not None:
        image_bytes = image_file.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Procesamiento de cada número
    total = len(numbers_df)
    
    for index, row in numbers_df.iterrows():
        try:
            phone_number = str(row[phone_column]).strip()
            
            # Eliminar caracteres no numéricos (excepto el signo +)
            clean_number = ''.join(c for c in phone_number if c.isdigit() or c == '+')
            
            # Asegurarse de que el número esté en formato internacional
            if clean_number.startswith('+'):
                clean_number = clean_number[1:]  # Quitar el signo +
                
            # Enviar mensaje de texto si existe
            success = True
            message_id = ""
            
            if message_text:
                text_endpoint = f"{api_url}/message/sendText/{instance_name}"

                payload = {
                    "number": clean_number,
                    "options": {
                        "delay": 5000,
                        "presence": "composing"
                    },
                    "text": message_text
                }
                
                response = requests.post(text_endpoint, headers=headers, json=payload)
                
                if response.status_code != 200 and response.status_code != 201:
                    success = False
                    errors += 1
                    error_msg = f"Error al enviar mensaje de texto a {clean_number}: {response.text}"
                    logs.append({"number": clean_number, "status": "ERROR", "details": error_msg})
                else:
                    message_id = response.json().get("key", {}).get("id", "Unknown")
            
            # Enviar imagen si existe
            if success and image_file is not None:
                media_endpoint = f"{api_url}/message/sendMedia/{instance_name}"
                
                filename = image_file.name
                filetype = f"image/{filename.split('.')[-1]}"

                media_payload = {
                    "number": clean_number,
                    "options": {
                        "delay": 5000
                    },
                    "mediatype": "image",
                    "caption": caption if caption else "",
                    "media": image_base64
                }
                
                response = requests.post(media_endpoint, headers=headers, json=media_payload)
                
                if response.status_code != 200 and response.status_code != 201:
                    success = False
                    errors += 1
                    error_msg = f"Error al enviar imagen a {clean_number}: {response.text}"
                    logs.append({"number": clean_number, "status": "ERROR", "details": error_msg})
            
            if success:
                successful += 1
                logs.append({"number": clean_number, "status": "OK", "messageId": message_id})
            
            # Actualizar progreso
            progress = (index + 1) / total
            progress_bar.progress(progress)
            status_text.text(f"Procesando {index+1} de {total} - Éxitos: {successful}, Errores: {errors}")
            
            # Delay para evitar bloqueos
            # Genera un delay aleatorio entre 10 y el valor de 'delay'
            delay_aleatorio = random.randint(10, delay)  # Incluye ambos extremos
            time.sleep(delay_aleatorio)
            
        except Exception as e:
            errors += 1
            error_msg = f"Error al procesar número {phone_number}: {str(e)}"
            logs.append({"number": phone_number, "status": "ERROR", "details": error_msg})
            status_text.text(f"Procesando {index+1} de {total} - Éxitos: {successful}, Errores: {errors}")
    
    progress_bar.progress(1.0)
    
    # Mostrar resultados finales
    if successful > 0:
        st.success(f"✅ {successful} mensajes enviados correctamente")
    
    if errors > 0:
        st.error(f"❌ {errors} mensajes fallaron")
    
    # Mostrar logs detallados
    st.subheader("Registro de envíos")
    logs_df = pd.DataFrame(logs)
    st.dataframe(logs_df)
    
    # Opción para descargar el registro
    csv = logs_df.to_csv(index=False)
    st.download_button(
        label="Descargar registro CSV",
        data=csv,
        file_name="whatsapp_envios_log.csv",
        mime="text/csv"
    )

# Botón para enviar mensajes
if numbers_df is not None:
    st.header("Paso 3: Enviar mensajes")
    send_button = st.button("Enviar mensajes masivos", type="primary")
    
    if send_button:
        with st.spinner("Enviando mensajes..."):
            send_messages()

# Información adicional
with st.expander("Información adicional"):
    st.markdown("""
    ### Configuración de la API
    - URL de Evolution API: Asegúrate de que la URL de la API sea correcta y esté accesible.
    - Nombre de la instancia: Debe coincidir con el nombre de tu instancia en Evolution API.
    - API Key: Si tu API requiere autenticación, asegúrate de incluir la API Key en el campo correspondiente, el cual lo encuentras justo debajo del nombre de la instancia.
    - Retraso entre mensajes (segundos): Ajusta el retraso según tus necesidades, pero ten en cuenta que un retraso muy corto puede resultar en bloqueos por parte de WhatsApp.
    
    ### Formato de números
    - Los números deben incluir el código de país sin el signo '+' (ej: 5215512345678)
    - Asegúrate de que el formato sea consistente en todo el archivo
    
    ### Consejos para evitar bloqueos
    - Usa un retraso adecuado entre mensajes (recomendado: 3-5 segundos)
    - No envíes a demasiados números desconocidos en poco tiempo
    - Es recomendable empezar con lotes pequeños para probar
    
    ### Sobre Evolution API
    - Asegúrate de que tu instancia está correctamente configurada y la sesión de WhatsApp activa
    - Consulta la documentación oficial para más información:
    - [Envío de texto](https://doc.evolution-api.com/v1/api-reference/message-controller/send-text)
    - [Envío de multimedia](https://doc.evolution-api.com/v1/api-reference/message-controller/send-media)
    """)
    
# Información del pie de página
st.markdown("---")
st.caption("Desarrollado por Hector")