from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = None
model_info = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global model, model_info
    
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file được tải lên'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File chưa được chọn'}), 400
    
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Chỉ chấp nhận file Excel (.xlsx)'}), 400
    
    try:
        df = pd.read_excel(file)
        
        if 'midterm' not in df.columns or 'final' not in df.columns:
            return jsonify({'error': 'File phải chứa cột "midterm" và "final"'}), 400
        
        x = df[['midterm']]
        y = df['final']
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2)
        
        model = LinearRegression()
        model.fit(x_train, y_train)
        
        train_score = model.score(x_train, y_train)
        test_score = model.score(x_test, y_test)
        
        train_pred = model.predict(x_train)
        test_pred = model.predict(x_test)
        train_mse = mean_squared_error(y_train, train_pred)
        test_mse = mean_squared_error(y_test, test_pred)
        
        model_info = {
            'train_score': float(train_score),
            'test_score': float(test_score),
            'train_mse': float(train_mse),
            'test_mse': float(test_mse),
            'slope': float(model.coef_[0]),
            'intercept': float(model.intercept_),
            'total_samples': len(df),
            'train_samples': len(x_train),
            'test_samples': len(x_test)
        }
        
        return jsonify({'success': True, 'message': 'Huấn luyện mô hình thành công!', 'info': model_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    global model
    
    if model is None:
        return jsonify({'error': 'Vui lòng tải lên file dữ liệu trước'}), 400
    
    try:
        data = request.get_json()
        midterm_score = float(data.get('midterm', 0))
        
        if midterm_score < 0 or midterm_score > 10:
            return jsonify({'error': 'Điểm giữa kỳ phải từ 0-10'}), 400
        
        input_data = np.array([[midterm_score]])
        predicted_score = model.predict(input_data)[0]
        
        return jsonify({
            'success': True,
            'midterm': midterm_score,
            'predicted': float(predicted_score)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
