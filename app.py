from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
from docx import Document
import os

app = Flask(__name__)

# Set upload folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["image"]

        if file:

            # Save uploaded image
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(image_path)

            # OCR
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang="eng")

            # Create Word file
            doc = Document()
            doc.add_paragraph(text)

            output_path = os.path.join(
                app.config["OUTPUT_FOLDER"],
                "output.docx"
            )

            doc.save(output_path)

            # Send file to user
            return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
