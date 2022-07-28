from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def get_root():
    return render_template('index.html')


@app.route('/api/rate')
def get_rate():
    return jsonify(todo=True)


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')  # noqa
    return jsonify(todo=True)


@app.route('/api/sendEmails', methods=['POST'])
def send_emails():
    return jsonify(todo=True)


app.run(debug=False)
