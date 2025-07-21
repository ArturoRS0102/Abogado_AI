import os
import openai
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from flask import render_template


load_dotenv()
app = Flask(__name__)
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
        prompt_sistema = f"""
Eres un asistente legal de inteligencia artificial, experto en leyes mexicanas y altamente capacitado en múltiples ramas del Derecho (civil, penal, laboral, administrativo, fiscal, familiar, etc.).
Tu función es exclusivamente brindar una orientación informativa general, **NO ofreces asesoría jurídica personalizada ni sustituyes la opinión de un abogado certificado**.

La consulta del usuario se contextualiza en la siguiente ubicación:
- País: {pais}
- Estado: {estado}
- Municipio: {municipio}

Instrucciones clave que NO debes romper:
1. **NO brindes asesoría formal ni te presentes como abogado.**
2. **NO prometas soluciones ni realices análisis jurídicos complejos.**
3. **Ofrece solo una explicación general del marco legal aplicable y posibles pasos, de forma clara y neutral.**
4. **Si la pregunta no tiene relación jurídica clara o no puedes dar una orientación segura, responde con cortesía que el usuario debe acudir a un abogado.**
5. **Siempre finaliza tu respuesta con esta advertencia obligatoria:**
   "Recuerda, esta es solo una orientación general y no sustituye la consulta con un abogado profesional o autoridad competente."

Tu objetivo es ayudar al usuario a entender de forma básica qué tipo de derecho está involucrado, qué conceptos legales podrían aplicar, y qué autoridades o profesionales pueden ayudarle.

Sé claro, profesional, breve y evita tecnicismos innecesarios.
"""


        response = openai.chat.completions.create(
    model="gpt-4o",  # Mucho mejor comprensión y precisión legal
    messages=[
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": pregunta}
    ],
    max_tokens=600,  # Aumentado para evitar respuestas incompletas
    temperature=0.4,  # Menos creatividad, más precisión

        )
        
        respuesta_ia = response.choices[0].message.content.strip()
        return jsonify({"respuesta": respuesta_ia})

    except Exception as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return jsonify({"error": "Hubo un problema al contactar al asistente. Inténtalo de nuevo."}), 500

# --- RUTA DE VERIFICACIÓN (LA IMPORTANTE) ---
@app.route('/monetization-sw.js') # <-- DEBE COINCIDIR CON EL NOMBRE DE TU ARCHIVO
def serve_service_worker():
    """ Sirve el archivo Service Worker desde la carpeta static. """
    return send_from_directory('static', 'monetization-sw.js')

@app.route("/terminos_condiciones")
def terminos_condiciones():
    return render_template("terminos_condiciones.html")



# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    app.run(debug=True)