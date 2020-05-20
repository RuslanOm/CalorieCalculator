from flask import Flask
from flask import render_template
from flask import request
import json


app = Flask(__name__, static_folder='static2')


with open("data/data.json", "r") as read_file:
    data = json.load(read_file)

# использовал для создания заполненности базы продуктов
# for i in range(10000):
#     data[str(i)] = i


def process_input(st):
    key, val = st.rsplit(maxsplit=1)
    data[key] = float(val)
    # для тестов нагрузки при добавлении элемента
    # del data[key]


def process_food(st):
    goods = st.split(";")
    res = 0
    ans = set()
    for item in goods:
        key, val = item.rsplit(maxsplit=1)
        val = float(val)
        if key not in data:
            ans.add(key)
        else:
            res += (data[key] / 100) * val
    return ans, res


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "CalcInput" in request.form:
            prod = request.form['CalcInput']
            process_input(prod)
            return render_template('index.html', added=True, ls=sorted(list(data.keys())))
        if "FoodInput" in request.form:
            goods = request.form["FoodInput"]
            not_in_data, res = process_food(goods)
            if not_in_data:
                return render_template("index.html", dt=not_in_data, ls=sorted(list(data.keys())))
            return render_template("index.html", result=res, ls=sorted(list(data.keys())))
        if "seldata" in request.form:
            mult = float(request.form["Weight"]) if request.form["Weight"] else 1
            return render_template("index.html", result=data[request.form["seldata"]] * mult / 100,
                                   ls=sorted(list(data.keys())))

    return render_template('index.html', ls=sorted(list(data.keys())))


@app.route('/about', methods=["GET"])
def about(name=None):
    return render_template('about.html', name=name)
