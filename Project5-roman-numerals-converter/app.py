from flask import Flask, render_template, request

app = Flask(__name__)

def convert(decimal_num):
    roman = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
    num_to_roman = ''
    for i in roman.keys():
        num_to_roman += roman[i] * (decimal_num // i)
        decimal_num %= i #decimal_num = decimal_num % i
    return num_to_roman

@app.route('/', methods=['GET'])
def main_get():
    return render_template('index.html', not_valid = False, developer_name = 'Baur')

@app.route('/', methods=['POST'])
def main_post():
    alphanumeric = request.form['number']
    if not alphanumeric.isdecimal():
        return render_template('index.html', not_valid=True, developer_name='Baur')
    number = int(alphanumeric)
    if not (0 < number < 4000):
        return render_template('index.html', not_valid=True, developer_name='Baur')
    return render_template('result.html', number_decimal=number, number_roman=convert(number), developer_name='Baur')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
