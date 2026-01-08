from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from spellchecker import SpellChecker
import re

tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")
spell = SpellChecker()

def clean_ocr_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

def spell_correct_text(text):
    corrected_words = []
    for word in text.split():
        corrected = spell.correction(word)
        corrected_words.append(corrected if corrected else word)
    return ' '.join(corrected_words)

def correct_text(text):
    precleaned = clean_ocr_text(text)
    spell_fixed = spell_correct_text(precleaned)
    input_text = "fix: " + spell_fixed  # <---- This line was wrong
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected

