from flask import Flask, render_template, request
from deepface import DeepFace
import os

app = Flask(__name__)
# Define a route to render the upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return render_template('upload.html', message='No file part')
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return render_template('upload.html', message='No selected file')
    
    if file:
        # Save the file to a temporary location
        filename = file.filename
        file_path = os.path.join("uploads", filename)
        file.save(file_path)
        
        # Analyze the uploaded image using DeepFace
        try:
            result = DeepFace.analyze(file_path, actions=['gender', 'age', 'emotion'])
            gender = result[0]['dominant_gender']
            age = result[0]['age']
            emotion = result[0]['dominant_emotion'].capitalize()
            
            # Delete the uploaded image file
            os.remove(file_path)
            
            # Render the result page with predictions
            return render_template('result.html', filename=filename, gender=gender, age=age, emotion=emotion)
        except Exception as e:
            # Delete the uploaded image file if an error occurs
            return render_template('upload.html', message='Error analyzing image: {}'.format(str(e)))

if __name__ == '__main__':
    app.run(debug=True)
