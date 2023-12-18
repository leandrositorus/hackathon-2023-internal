import sys
import os
# sys.path.append("..")

from flask import Flask, render_template, request, jsonify
from working_code.run_dalle import generate_ai

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
TARGET_FOLDER = './targets'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TARGET_FOLDER'] = TARGET_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/processor', methods=['GET', 'POST'])
def processor():
    if request.method == 'POST':
        # Access form data
        image_file = request.files['input_picture']
        prompt_text = request.form['prompt']
        product_name = request.form['product_name']
        description = request.form['description']
        price = request.form['price']
        option_value = request.form['options']

        if image_file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(filename)

        # result = generate_ai(filename, prompt_text, product_name, description, price)

        # Process the form data as needed
        # For now, just printing the values
        print('Image File:', image_file)
        print('Prompt:', prompt_text)
        print('Product Name:', product_name)
        print('Description:', description)
        print('Price:', price)
        print('Option Value:', option_value)

        response_data = {
            'status': 'success',
            'message': 'Form submitted successfully!',
            'data': {
                'image_file': image_file.filename,
                'prompt_text': prompt_text,
                'product_name': product_name,
                'description': description,
                'price': price,
                'option_value': option_value,
            }
        }

        return jsonify(response_data)

    return render_template('processor.html')

if __name__ == '__main__':
    app.run(debug=True)
