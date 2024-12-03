from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'secret_key_for_flask'

# Creează folderul pentru fișierele încărcate dacă nu există
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csvfile' not in request.files:
        flash('Niciun fișier nu a fost selectat!', 'error')
        return redirect(url_for('index'))

    file = request.files['csvfile']
    if file.filename == '':
        flash('Niciun fișier nu a fost selectat!', 'error')
        return redirect(url_for('index'))

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash('Fișierul a fost încărcat cu succes!', 'success')
        return redirect(url_for('display_data', filename=file.filename))

    flash('Vă rugăm să încărcați un fișier CSV valid!', 'error')
    return redirect(url_for('index'))

@app.route('/data/<filename>')
def display_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        flash(f"Eroare la citirea fișierului: {e}", 'error')
        return redirect(url_for('index'))

    table_html = df.head(10).to_html(classes='table table-striped', index=False)
    return render_template('data.html', table=table_html, filename=filename)

@app.route('/analyze/<filename>', methods=['POST'])
def analyze_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)

    operation = request.form.get('operation')
    column = request.form.get('column')

    if operation == 'mean':
        result = df[column].mean()
    elif operation == 'sum':
        result = df[column].sum()
    else:
        result = "Operație necunoscută!"

    flash(f"Rezultatul operației {operation} pe coloana '{column}' este: {result}", 'success')
    return redirect(url_for('display_data', filename=filename))

if __name__ == '__main__':
    app.run(debug=True)
