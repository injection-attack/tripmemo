# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# todos = []

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/todos', methods=['GET', 'POST'])
# def manage_todos():
#     if request.method == 'GET':
#         return jsonify(todos)
#     elif request.method == 'POST':
#         todo = request.json
#         todos.append(todo)
#         return jsonify(todo), 201

# @app.route('/api/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
# def manage_todo(todo_id):
#     if request.method == 'PUT':
#         if 0 <= todo_id < len(todos):
#             todos[todo_id]['completed'] = not todos[todo_id]['completed']  # 토글 로직
#             return jsonify(todos[todo_id])
#         return jsonify({"error": "Todo not found"}), 404
#     elif request.method == 'DELETE':
#         if 0 <= todo_id < len(todos):
#             deleted_todo = todos.pop(todo_id)
#             return jsonify(deleted_todo)
#         return jsonify({"error": "Todo not found"}), 404

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

todos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET', 'POST'])
def manage_todos():
    global todos
    if request.method == 'GET':
        return jsonify(todos)
    elif request.method == 'POST':
        todo = request.json
        todo['completed'] = False
        todos.append(todo)
        return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
def manage_todo(todo_id):
    global todos
    try:
        if request.method == 'PUT':
            if 0 <= todo_id < len(todos):
                todos[todo_id]['completed'] = not todos[todo_id]['completed']
                print(f"Updated todo: {todos[todo_id]}")  # 디버깅용 출력
                return jsonify(todos[todo_id])
            return jsonify({"error": "Todo not found"}), 404
        elif request.method == 'DELETE':
            if 0 <= todo_id < len(todos):
                deleted_todo = todos.pop(todo_id)
                return jsonify(deleted_todo)
            return jsonify({"error": "Todo not found"}), 404
    except Exception as e:
        print(f"Error in manage_todo: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

