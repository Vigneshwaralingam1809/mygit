from flask import Flask, request, render_template_string, redirect, send_file
import pandas as pd
from test import main
from flask import Flask
app = Flask(__name__)  # Make sure your app instance is named 'app'

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Git Tracker Mailer</title>
<h1>📩 Git Push Tracker Email System</h1>
<form method=post enctype=multipart/form-data>
  <label>Upload git.xlsx file:</label>
  <input type=file name=file required>
  <input type=submit value="Send Emails and Update File">
</form>
<br>
{% if table %}
  <h2>Processed Data:</h2>
  {{ table | safe }}
  <br><a href="/download">Download Updated Excel</a>
{% endif %}
'''

updated_file_path = "gitusers_updated.xlsx"

@app.route('/', methods=['GET', 'POST'])
def upload_and_process():
    table = None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.xlsx'):
            uploaded_file.save('git.xlsx')
            main()
            df = pd.read_excel(updated_file_path)
            table = df.to_html(classes='data', header="true", index=False)
        else:
            return "❌ Please upload an .xlsx file only."
    return render_template_string(HTML, table=table)

@app.route('/download')
def download_file():
    return send_file(updated_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
