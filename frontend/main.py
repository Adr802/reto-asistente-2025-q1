import base64
import gradio as gr
import requests

# Función para convertir un archivo a base64
def convertir_a_base64(archivo):
    try:
        with open(archivo, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        return encoded_string
    except Exception as e:
        return f"Error al convertir el archivo: {e}"

# Función que realiza una solicitud al endpoint externo
def obtener_respuesta_externa(mensaje):
    url = "http://orchestration:8080/orchestrate"

    # Validar que el mensaje de texto no esté vacío
    if not mensaje.get("text"):
        return "El mensaje de texto no puede estar vacío."

    payload = {"query": mensaje["text"]}

    # Si hay un archivo adjunto, procesarlo
    archivos = mensaje.get("files", [])
    if archivos:
        archivo = archivos[0]
        if archivo.endswith(".pdf"):
            pdf_encode = convertir_a_base64(archivo)
            if pdf_encode.startswith("Error"):
                return pdf_encode
            payload["pdf_encode"] = pdf_encode
        else:
            return "El archivo debe ser un PDF."

    try:
        respuesta = requests.post(url, json=payload)
        if respuesta.status_code == 200:
            return respuesta.json().get("response", {}).get("assistant_response", "No se encontró una respuesta válida.")
        else:
            return f"Error en la solicitud: {respuesta.status_code}"
    except requests.RequestException as e:
        return f"Error de conexión: {e}"

# Función que maneja la interacción del chat
def manejar_mensaje(mensaje, historial):
    respuesta = obtener_respuesta_externa(mensaje)
    return respuesta

# Crear la interfaz de chat
demo = gr.ChatInterface(
    manejar_mensaje,
    type="messages",
    autofocus=False,
    multimodal=True,
    title = "AurelioAsistente",
    description = "¡Hola! Soy AurelioAsistente, tu aliado financiero personal. Estoy aquí para ayudarte a gestionar tus finanzas de manera eficiente y segura. Puedo analizar tus estados de cuenta y ofrecerte recomendaciones personalizadas para que tomes decisiones informadas. Además, al considerar opciones de compra en comercios ecuatorianos, te ayudo a encontrar las mejores ofertas disponibles.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)