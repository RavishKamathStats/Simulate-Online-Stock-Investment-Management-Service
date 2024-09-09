from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource
import yfinance as yf
from yfinance_helper import get_info
from sqlalc import get_record, add_record

app = Flask(__name__)
api = Api(app)

global_stock_name = ''

def change_stock(input_stock):
    global global_stock_name
    global_stock_name = input_stock

def get_stockname():
    return global_stock_name

# notice the functions under each @ cannot be same, otherwise, overwritting error happens
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/get_stock/', methods=['GET', 'POST'])
def get_stock():
    stock_name = request.form['fname']
    
    change_stock(stock_name)

    # yahoo fincance api call
    #print('stock name: ', stock_name) # try GOOGL
    ticker = yf.Ticker(stock_name).info['sector']
    #print("sector: ", ticker)
    info_list = get_info(stock_name)
    current_price = round(info_list[0],2)

    return render_template('result.html', fname=stock_name, current_price=current_price, type=ticker)

@app.route('/buy_stock/', methods=['GET', 'POST'])
def put_stock():
    ticker = yf.Ticker(global_stock_name).info['sector']
    stock_buy = request.form['stock_buy']
    print('stock buy: ', stock_buy)

    info_dict = get_info(global_stock_name)
    open_price = info_dict[0]
    high_price = info_dict[1]
    low_price = info_dict[2]
    close_price = info_dict[3]

    add_record(20, global_stock_name, open_price, open_price, close_price, stock_buy, -1)
    record_df = get_record()

    return render_template('result.html', fname=global_stock_name, current_price=open_price, type=ticker, record=record_df.to_html())

@app.route('/sell_stock/', methods=['GET', 'POST'])
def sell_stock():
    ticker = yf.Ticker(global_stock_name).info['sector']
    stock_sell = request.form['stock_sell']
    print('stock sell: ', stock_sell)

    info_dict = get_info(global_stock_name)
    open_price = info_dict[0]
    high_price = info_dict[1]
    low_price = info_dict[2]
    close_price = info_dict[3]

    add_record(9, global_stock_name, open_price, open_price, close_price, -1, stock_sell)

    return render_template('result.html', fname=global_stock_name, current_price=open_price, type=ticker)


@app.route('/update_stock/', methods=['GET', 'POST'])
def update_stock():
    return render_template('result.html')

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
#%%

#%%
