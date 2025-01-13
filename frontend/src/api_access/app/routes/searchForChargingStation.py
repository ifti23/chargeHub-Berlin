from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/search_station_plz', methods=['GET'])
def search_station_plz():
    search_id = request.args.get('plz', type=int)
    if not 10114 < search_id < 14200:
        return jsonify({"error": "The given postal code needs to be from berlin (between 10115 and 14199)"}), 400

    return jsonify({"message": "Hello from the backend!"})



if __name__ == '__main__':
    app.run(debug=True)