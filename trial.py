from flask import Flask, render_template, request, send_file
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO
import os

app = Flask(__name__)

# Configure Google Gemini API Key using an environment variable
genai.configure(api_key="AIzaSyC5BVYL55poCffhsWB034hQQnVB3X0wf-E")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    try:
        # Get user inputs from form
        name = request.form['name']
        linkedin = request.form['linkedin']
        phone = request.form['phone']
        email = request.form['email']
        job_description = request.form['job_description']

        # Generate resume content using Google Gemini API
        prompt = (f"Generate a professional resume for {name}, "
                  f"contact information: {phone}, {email}, "
                  f"LinkedIn: {linkedin}. Job description: {job_description}.",
                  '''
                  There are few things I would like you to keep in mind:-
                  1. The resume should be in a standard format.
                  2. The resume should be in a standard font.
                  3. The resume should be in a standard size.
                  4. The resume should be in a standard layout.
                  5. The resume should strictly be of 1 page only.
                  6. Name should be written on the top the the resume in bigger font and phone number, email and linkedin profile right below it in smaller font.
                  7. Resume should be ATS friendly, hence it should insanely match the given Job Description.
                  8. There should be a line which will divide each section of the resume.
                  9. Email, mobile number and linkedin profile, all should be in one line.
                  10. You shall not include the *Note* at the end of the resume.
                  11. Line between the section should be big enough like the width of the page
                  ''')
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Call the API and get the response
        response = model.generate_content(prompt)

        # Access generated text correctly (adjust according to the response structure)
        resume_content = response.text  # Change this if the response structure differs

        # Create PDF in memory
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in resume_content.split('\n'):
            pdf.multi_cell(0, 10, line)

        # Save PDF to a temporary file
        temp_pdf_path = "temp_resume.pdf"  # Define a temporary file name
        pdf.output(temp_pdf_path)  # Save to file

        # Read the PDF file into BytesIO
        with open(temp_pdf_path, 'rb') as f:
            pdf_bytes = BytesIO(f.read())

        # Remove the temporary file after reading
        os.remove(temp_pdf_path)

        # Send the PDF as an attachment
        return send_file(pdf_bytes, as_attachment=True, download_name="resume.pdf", mimetype='application/pdf')

    except Exception as e:
        # Return an error message and HTTP 500 status code
        return f"Error generating resume: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)