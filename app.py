import os
import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from googletrans import Translator

# Initialize Flask app
app = Flask(__name__)

# Initialize Translator
translator = Translator()

# Set your Groq API key and Groq API base URL
GROQ_API_KEY = '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'  # Replace with your actual Groq API key
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# Function to scrape content from a URL
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        return f"Error scraping {url}: {e}"

# Scrape content from the specified websites
fitwellhub_pk_content = scrape_website('https://fitwellhub.pk/')
fitwellhub_com_content = scrape_website('https://fitwellhub.com/')
ss_group_content = scrape_website('https://www.ssgroup.pk/')

# Combine all content
combined_content = f"{fitwellhub_pk_content}\n{fitwellhub_com_content}\n{ss_group_content}"

# Function to call Groq API directly
def call_groq_api(prompt):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Answer accurately based on the provided website information."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error from Groq API: {response.text}"

# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    response = ''
    if request.method == 'POST':
        user_input = request.form['user_input']

        # Detect language synchronously
        detected_lang = translator.detect(user_input)
        if detected_lang.lang != 'en':
            user_input_en = translator.translate(user_input, src=detected_lang.lang, dest='en').text
        else:
            user_input_en = user_input

        prompt = f"Based on the following information:\n{combined_content}\n\nAnswer the question: {user_input_en}"

        try:
            answer_en = call_groq_api(prompt)
        except Exception as e:
            answer_en = f"Error generating response: {e}"

        if detected_lang.lang != 'en':
            response = translator.translate(answer_en, src='en', dest=detected_lang.lang).text
        else:
            response = answer_en

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
