from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from utils.gemini_handler import analyze_image
import base64

app = Flask(__name__)

# アップロード設定
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB制限

# アップロードフォルダの作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': '画像がアップロードされていません'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '許可されていないファイル形式です'}), 400
    
    try:
        # ファイルを保存
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 画像分析
        result = analyze_image(filepath)
        
        # 画像をbase64エンコード
        with open(filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 一時ファイルを削除
        os.remove(filepath)
        
        return jsonify({
            'feature': result['feature'],
            'description': result['description'],
            'image': img_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 