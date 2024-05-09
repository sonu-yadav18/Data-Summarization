import requests
from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html", result="")

@app.route("/Summarize", methods=["POST"])
def Summarize():
    # Check if text is pasted
    if 'data' in request.form:
        text = request.form["data"]
    else:
        text = ""
    
    # Check if file is uploaded
    if 'document' in request.files:
        document = request.files['document']
        # Check if the file is a PDF
        if document.filename.endswith('.pdf'):
            pdfReader = PyPDF2.PdfFileReader(document)
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                text += pageObj.extractText()
        # Check if the file is a text file
        elif document.filename.endswith('.txt'):
            text += document.read().decode('utf-8')
        else:
            return render_template("index.html", result="", error="Unsupported file format")

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer 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"}

    maxL = int(request.form["maxL"])
    minL = maxL // 4
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": text,
        "parameters": {"min_length": minL, "max_length": maxL},
    })[0]
    
    return render_template("index.html", result=output["summary_text"])

if __name__ == '__main__':
    app.run(debug=True)
