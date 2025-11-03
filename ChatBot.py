import streamlit as st
from groq import Groq
st.set_page_config(page_title="Mi chat de IA", layout ="centered", page_icon="😠")

st.title("Mi primer aplicacion con Streamlit. ")

nombre = st.text_input("!Cual es tu nombre?")

if st.button("Saludar"):
    st.write(f"Hola {nombre}")

    #clase 7
#1ro es crear un archivo en nuestra carpeta principal que se va a llamar secrets.toml

    
MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

#creamos una lista con los odelos de IA de groq que vamos a usar
def configurar_pagina():
    #agregamos un titulo principal a donde va a estar el historial
    st.title("Mi chat de IA")
    st.sidebar.title("Configuracion del modelo")
    elegirModelo = st.sidebar.selectbox('Elegi el modelo de IA', options = MODELOS, index = 0)
    return elegirModelo

#funcion para crear un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets ["clave_api"]
    return Groq (api_key=clave_secreta)

#funcion configurar modelo de mensaje o de entrada
def configurar_modelo(cliente, modelo, mensajedeentrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role" : "user", "content": mensajedeentrada}],
        stream=True 
    )

#creamos una funcion que nos permita hacer uso del historial. es decir, recordar los mensajes anteriores.

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
  #Clase 8
    #Actualizar historial
def actualizar_historial(rol, contenido,avatar):
    st.session_state.mensajes.append({"role": rol, "content":contenido, "avatar":avatar})
  
    #Mostrar historial
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = ["avatar"]):
            st.markdown(mensaje["content"])

#Area del historial
def area_historial():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()
#Clase 9
#Funcion generar_respuesta() 
def generar_respuesta(chat_completo):
    #Crear una variable string vacia
    respuesta_completa = ""
    for frase in chat_completo: 
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


#Funcion main()

def main():
    elegirModelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_historial()
    mensaje = st.chat_input("Escribi tu mensaje")
    if mensaje:
        actualizar_historial("user", mensaje, "😎")
        chat_completo = configurar_modelo(clienteUsuario, elegirModelo , mensaje)
        if chat_completo:
            with st.chat_message("assitant"):
                chat_completo = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assitant", chat_completo, "🤖")
    st.rerun()

if __name__ == "__main__":
    main()


    

