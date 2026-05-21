from flask import Flask, render_template, request
from transformers import T5ForConditionalGeneration, T5Tokenizer
from deep_translator import GoogleTranslator  # অনুবাদ করার জন্য লাইব্রেরি

app = Flask(__name__)

# AI model
model_name = "vennify/t5-base-grammar-correction"

# মডেল এবং টোকেনাইজার লোড করা হচ্ছে
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def correct_text(text):
    input_text = "grammar: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(inputs, max_length=256, num_beams=5)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


@app.route("/", methods=["GET", "POST"])
def home():
    original = ""
    result = ""
    translation = ""  # নতুন ভ্যারিয়েবল

    if request.method == "POST":
        original = request.form["text"]
        result = correct_text(original)  # আপনার এআই মডেল দিয়ে গ্রামার ঠিক করা হলো
        
        # ঠিক করা ইংরেজি বাক্যটিকে পাইথন দিয়ে বাংলায় অনুবাদ করা হচ্ছে
        try:
            translation = GoogleTranslator(source='en', target='bn').translate(result)
        except Exception:
            translation = "অনুবাদ করা যায়নি।"

    # আপনার index.html ফাইলে translation-ও পাঠিয়ে দেওয়া হলো
    return render_template("index.html", original=original, result=result, translation=translation)


if __name__ == "__main__":
    app.run(debug=True)