import os
import openai
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Cargar variables de entorno (importante para la API key)
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la API Key de OpenAI desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- RUTAS DE LA APLICACIÓN ---

@app.route("/")
def index():
    """ Sirve la página principal (index.html). """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """ Recibe la consulta del usuario y devuelve la respuesta de OpenAI. """
    data = request.json
    pais = data.get("pais")
    estado = data.get("estado")
    municipio = data.get("municipio")
    pregunta = data.get("pregunta")

    if not pregunta:
        return jsonify({"error": "La pregunta no puede estar vacía."}), 400

    try:
        # Construcción del Prompt para guiar a la IA
        prompt_sistema = f"""
        Actúa como un asistente legal informativo para México. Tu propósito es ofrecer orientación general y educativa sobre posibles acciones a tomar.
        NO ofreces asesoramiento legal formal y siempre debes recordarle al usuario que consulte a un abogado certificado.
        La consulta del usuario se enmarca en la siguiente jurisdicción:
        - País: {pais}
        - Estado: {estado}
        - Municipio/Ciudad: {municipio}

        Basa tu respuesta en la legislación aplicable a esta ubicación, si es posible.
        Mantén tus respuestas concisas, claras y no excedas los 200 tokens.
        Finaliza SIEMPRE con la siguiente advertencia: 'Recuerda, esta es una orientación informativa y no sustituye la consulta con un abogado profesional.'
        """

        # Llamada a la API de OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=200,
            temperature=0.5,
        )
        
        respuesta_ia = response.choices[0].message.content.strip()
        return jsonify({"respuesta": respuesta_ia})

    except Exception as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return jsonify({"error": "Hubo un problema al contactar al asistente. Inténtalo de nuevo."}), 500

@app.route('/propellerads.txt')
def serve_verification_file():
    """ Sirve el archivo de verificación para la monetización. """
    # Asegúrate de que tu archivo de verificación esté en la carpeta 'static'
    return send_from_directory('static', 'propellerads.txt')

# --- INICIO DE LA APLICACIÓN ---

if __name__ == "__main__":
    # Esto es solo para pruebas locales. Render usará Gunicorn.
    app.run(debug=True)