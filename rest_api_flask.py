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

if __name__ == '__main__':
    app.run(debug=True)
