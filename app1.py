from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_siri')
def run_siri():
    try:
        subprocess.Popen(["python", "app.py"])
        return "Desi Siri chalu ho gaya!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
