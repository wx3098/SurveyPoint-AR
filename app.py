from flask import Flask, render_template, jsonify
from converter import xy_to_latlon

app = Flask(__name__)

def load_sima_points(filepath):
    """SIMAファイルを読み込んで緯度経度のリストを返す"""
    points = []
    # SIMAファイルは一般的に Shift-JIS です
    with open(filepath, mode='r', encoding='shift_jis') as f:
        reader = csv.reader(f)
        for row in reader:
            # 座標データ（A01レコード）のみを抽出
            if len(row) >= 5 and row[0] == "A01":
                try:
                    name = row[2].strip()  # 3列目が点名
                    x = float(row[3])      # 4列目がX
                    y = float(row[4])      # 5列目がY
                    
                    # 座標変換（converter.pyの関数を使用）
                    lat, lon = xy_to_latlon(x, y)
                    
                    points.append({
                        "name": name,
                        "lat": lat,
                        "lon": lon
                    })
                except ValueError:
                    # 数値変換できない行（ヘッダーなど）はスキップ
                    continue
    return points

@app.route('/api/points')
def get_points():
    # dataフォルダに置いたファイルを読み込む
    points = load_sima_points('data/観測データ.sim')
    return jsonify(points)
    
@app.route('/')
def index():
    # templates/index.html を表示させる
    return render_template('index.html')

# 座標データをJSON形式で返すAPI（あとでARで使います）
@app.route('/api/points')
def get_points():
    # 仮のデータ（本来はここで.simファイルを読み込む）
    sample_points = [
        {"name": "点1", "lat": 31.5, "lon": 130.5}
    ]
    return jsonify(sample_points)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)