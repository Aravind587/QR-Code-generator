import qrcode
import base64
from io import BytesIO
from flask import Flask, render_template_string, request

app = Flask(__name__)

def generate_qr(message):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    # Convert image to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}", buffer.getvalue()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: Arial, sans-serif;
            background-color: #5fc5ed;
            overflow: hidden;
        }
        h2 {
            margin-bottom: 20px;
        }
        form {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        input {
            padding: 10px;
            width: 250px;
            border: 1px solid white;
            border-radius: 25px;
            font-size: 16px;
            transition: border 0.3s, transform 0.3s;
        }
        input:hover {
           border: 2px solid white;
        }
        input:focus {
            transform: scale(1.05);
            border-color: #007bff;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: background 0.3s, transform 0.3s;
        }
        button:hover {
            background-color: #218838;
            transform: scale(1.1);
        }
        img {
            margin-top: 10px;
            border: 5px solid #333;
            padding: 10px;
            background: white;
            border-radius: 20px;
            animation: fadeIn 0.5s ease-in-out;
        }
        .share-buttons {
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        .download-button {
            padding: 10px 15px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .download-button:hover {
            background-color: #0056b3;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.5); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    <script>
        function downloadQRCode() {
            const qrImage = document.getElementById('qrImage');
            const link = document.createElement('a');
            link.href = qrImage.src;
            link.download = 'qrcode.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</head>
<body>
    <h2>Enter a message to generate a QR Code</h2>
    <form method="POST">
        <input type="text" name="message" placeholder="Enter your text" required>
        <button type="submit">Generate QR</button>
    </form>
    {% if qr_code_path %}
        <h3>Your QR Code:</h3>
        <img id="qrImage" src="{{ qr_code_path }}" alt="QR Code">
        <div class="share-buttons">
            <button class="download-button" onclick="downloadQRCode()">Download QR Code</button>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_path = None
    if request.method == 'POST':
        message = request.form['message']
        qr_code_path, _ = generate_qr(message)
    return render_template_string(HTML_TEMPLATE, qr_code_path=qr_code_path)

if __name__ == "__main__":
    app.run(debug=True)
