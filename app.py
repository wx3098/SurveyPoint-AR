import csv
import os
from flask import Flask, render_template, jsonify
from converter import xy_to_latlon

app = Flask(__name__)

def load_sima_points(filepath):
    """SIMAファイルを読み込んで緯度経度のリストを返す"""
    points = []
    if not os.path.exists(filepath):
        print(f"エラー: {filepath} が見つかりません")
        return points

    with open(filepath, mode='r', encoding='shift_jis') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 5 and row[0] == "A01":
                try:
                    name = row[2].strip()
                    x = float(row[3])
                    y = float(row[4])
                    lat, lon = xy_to_latlon(x, y)
                    points.append({"name": name, "lat": lat, "lon": lon})
                except (ValueError, IndexError):
                    continue
    return points

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/points')
def get_points():
    # dataフォルダ内のファイル名を指定
    points = load_sima_points('data/観測データ.sim')
    return jsonify(points)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)