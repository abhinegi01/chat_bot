from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure your generative AI model
api_key = os.getenv('GEMINI_API_KEY')  # Ensure GEMINI_API_KEY is set in your environment variables
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')  # Check if this is the correct model initialization for your library

# Define your 404 error handler to redirect to the index page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            question = prompt

            # Ensure that model has the correct method for content generation
            response = model.generate_text(prompt=question)

            if response.text:
                return response.text
            else:
                return "Sorry, but I think Gemini didn't want to answer that!"
        except Exception as e:
            return f"An error occurred: {str(e)}"  # More specific error message

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
