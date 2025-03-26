from flask import Flask, request, jsonify
from database import Database  

app = Flask(__name__)
db = Database()

@app.route('/submitData', methods=['POST'])
def submit_data():
    data = request.json  # Получаем JSON данные из запроса
    raw_data = data.get('raw_data')  # Извлекаем необходимые данные
    if not raw_data:
        return jsonify({"error": "raw_data is required"}), 400
    
    # Вставляем данные в базу
    record_id = db.submit_data(raw_data)
    return jsonify({"message": "Data submitted successfully", "id": record_id}), 201

@app.route('/submitData/<int:id>', methods=['GET'])
def get_data(id):
    """Получить одну запись (перевал) по её id."""
    record = db.get_data_by_id(id)
    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "Record not found"}), 404

@app.route('/submitData/<int:id>', methods=['PATCH'])
def update_data(id):
    """Отредактировать существующую запись, если она в статусе new."""
    data = request.json
    status = data.get('status')  # Получаем статус из запроса
    
    if status and status != 'new':
        return jsonify({"state": 0, "message": "Record can only be updated if status is 'new'."}), 400
    
    updated = db.update_data(id, data)
    if updated:
        return jsonify({"state": 1, "message": "Record updated successfully."}), 200
    else:
        return jsonify({"state": 0, "message": "Failed to update record."}), 400

@app.route('/submitData/', methods=['GET'])
def get_user_data():
    """Получить список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер."""
    email = request.args.get('user__email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    records = db.get_data_by_email(email)
    return jsonify(records), 200

if __name__ == '__main__':
    app.run(debug=True)