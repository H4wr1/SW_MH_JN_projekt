from flask import Flask, render_template, request
import similarity_measures

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []  
    if request.method == 'POST':
        user_input = request.form['user_input']
        print(f'Text received: {user_input}', flush=True)
        print('Calculating. Wait.', flush=True)
        result = similarity_measures.calculate_measures(user_input)
        # return f'Result: {result}'
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)