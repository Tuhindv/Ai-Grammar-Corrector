from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
from deep_translator import GoogleTranslator

app = Flask(__name__)

# টোকেন ছাড়াই ক্লায়েন্ট তৈরি করা
client = InferenceClient(model="grammarly/coedit-large")

def correct_grammar(text):
    try:
        # ইনপুট ফরম্যাট
        result = client.text_generation(f"gec: {text}")
        return result
    except:
        return text

def translate_to_bangla(text):
    try:
        return GoogleTranslator(source='auto', target='bn').translate(text)
    except:
        return "অনুবাদ সম্ভব হয়নি।"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correct', methods=['POST'])
def correct():
    data = request.get_json()
    input_text = data.get('text', '')
    
    corrected = correct_grammar(input_text)
    translated = translate_to_bangla(corrected)
    
    return jsonify({'corrected': corrected, 'translated': translated})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)