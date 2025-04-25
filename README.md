# Enviador Masivo de WhatsApp

Una aplicación de Streamlit para enviar mensajes masivos a través de WhatsApp utilizando Evolution API.

![Banner WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 📋 Características

- Envío de mensajes de texto masivos a números de WhatsApp
- Soporte para adjuntar imágenes a los mensajes
- Carga de números desde archivos CSV o Excel
- Interfaz de usuario intuitiva y fácil de usar
- Seguimiento en tiempo real del progreso de envío
- Registro detallado de éxitos y errores
- Control de retraso entre mensajes para prevenir bloqueos
- Modo de depuración para solucionar problemas

## 🚀 Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/hectorj88/Masivos-WhatsApp-Evolution-Api.git
   cd enviador-masivo-whatsapp
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```
   streamlit run app.py
   ```

## 📦 Requisitos

Asegúrate de tener instalados:

```
streamlit>=1.30.0
pandas>=2.0.0
requests>=2.25.0
```

Crea un archivo `requirements.txt` con estos paquetes.

## ⚙️ Configuración

Para utilizar esta aplicación, necesitas:

1. Una instancia de [Evolution API](https://github.com/evolution-api/evolution-api) correctamente configurada
2. Un número de WhatsApp escaneado y conectado a tu instancia
3. Acceso a la URL donde está alojada tu API

## 📝 Uso

1. **Configuración de la API**:
   - Introduce la URL de Evolution API
   - Especifica el nombre de tu instancia
   - Proporciona la API Key si la tienes configurada
   - Ajusta el retraso entre mensajes para evitar bloqueos

2. **Carga de contactos**:
   - Sube un archivo CSV o Excel con los números
   - Selecciona la columna que contiene los números
   - Revisa la vista previa de los datos

3. **Composición del mensaje**:
   - Escribe el mensaje a enviar
   - Opcionalmente, adjunta una imagen
   - Añade un pie de foto si lo deseas

4. **Envío y seguimiento**:
   - Haz clic en "Enviar mensajes masivos"
   - Sigue el progreso en tiempo real
   - Descarga el registro de resultados

## 📱 Formato de números

Los números deben estar en formato internacional sin el signo '+':
- ✅ Correcto: 573223216549
- ❌ Incorrecto: +573223216549
- ❌ Incorrecto: 3223216549

## ⚠️ Precauciones

- Enviar mensajes masivos a números desconocidos puede resultar en el bloqueo de tu cuenta de WhatsApp
- Comienza con pequeños lotes de prueba antes de enviar a grandes cantidades
- Utiliza retrasos apropiados entre mensajes (3-5 segundos recomendado)
- Esta herramienta debe usarse con responsabilidad y respetando las políticas de WhatsApp

## 📄 Documentación de la API

Esta aplicación utiliza [Evolution API](https://doc.evolution-api.com/) para interactuar con WhatsApp:
- [Documentación de envío de texto](https://doc.evolution-api.com/v1/api-reference/message-controller/send-text)
- [Documentación de envío de multimedia](https://doc.evolution-api.com/v1/api-reference/message-controller/send-media)

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, siente libre de abrir un issue o enviar un pull request.

## ❓ Preguntas frecuentes

### ¿Puedo enviar mensajes a cualquier número?
Sí, pero se recomienda enviar solo a números que hayan dado su consentimiento para recibir mensajes.

### ¿Puedo personalizar el mensaje para cada número?
Actualmente, la aplicación envía el mismo mensaje a todos los números. La personalización será añadida en futuras versiones.

### ¿Qué pasa si mi cuenta de WhatsApp se desconecta?
Necesitarás volver a escanear el código QR en tu instancia de Evolution API antes de continuar.

### ¿Cómo evito que WhatsApp bloquee mi cuenta?
Utiliza retrasos apropiados entre mensajes, no envíes a demasiados números desconocidos en poco tiempo, y asegúrate de que tu actividad cumpla con los términos de servicio de WhatsApp.

---

⭐ **Si te resulta útil, ¡no olvides darle una estrella en GitHub!** ⭐
