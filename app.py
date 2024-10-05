import hashlib

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import loginSQL
from flask import Flask, request, jsonify, render_template
import plotly.express as px
import os
from StatisticalAnalysis import StatisticalAnalysis
from SDES import SDES
import numpy as np
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 添加secret_key以启用flash功能

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user-register.html', methods=['GET'])
def user_register_page():
    return render_template('user-register.html')  # 渲染注册页面

@app.route('/check_user', methods=['GET'])
def check_user():
    username = request.args.get('username', '').strip()
    password = request.args.get('password', '').strip()

    if not username or not password:
        return render_template('index.html', error_message="用户名和密码不能为空")  # 处理空输入

    # 如果用户名不存在
    result = loginSQL.search_by_name(username)
    if not result:
        return render_template('index.html', error_message="用户不存在")  # 返回一个错误页面


    # 验证密码
    if password == result[2]:
        return render_template('system.html')  # 假设这是用户的主页面
    else:
        return render_template('index.html', error_message="密码错误")  # 返回错误信息



@app.route('/user-register', methods=['POST'])
def user_register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': "用户名和密码不能为空"})  # 处理空输入

    result = loginSQL.search_by_name(username)
    if not result:
        loginSQL.insert_user(username, password)  # 确保密码是安全存储的
        flash('注册成功，请登录！')  # 使用 flash 显示成功提示信息
        return jsonify({'success': True, 'redirect': url_for('index')})  # 注册成功
    else:
        return jsonify({'success': False, 'message': '用户已存在'})  # 用户已存在
# 路由：生成 scatter.html 文件
@app.route('/generate-scatter', methods=['POST'])
def generate_scatter():
    try:
        data = request.get_json()
        print('Received data:', data)  # 输出收到的数据
        plaintext_count = int(data.get('plaintextCount', 0))  # 获取前端传来的明密文对数

        # 参数验证
        if plaintext_count <= 0:
            print('Invalid plaintext_count:', plaintext_count)  # 输出无效值
            return jsonify({'error': '明密文对数必须为正整数'}), 400

        SA = StatisticalAnalysis()
        plainText_decimal, cipherText_decimal, key_decimal = SA.generateGroup(plaintext_count)  # 产生数据组

        # 根据输入生成散点图数据
        point_x = plainText_decimal
        point_y = cipherText_decimal

        # 生成 Plotly 图表
        fig = px.scatter(x=point_x, y=point_y,
                         title=f"Scatter Plot of Plaintext vs Ciphertext for {plaintext_count} Points")

        # 保存图表到 static 文件夹中的 scatter.html
        scatter_path = os.path.join('static', 'scatter.html')
        fig.write_html(scatter_path)

        # 相关性分析
        correlation_pc = SA.correlationAnalysis('P-C', 'Pearson')
        correlation_kc = SA.correlationAnalysis('K-C', 'Pearson')

        rho_pc, p_value_pc = SA.correlationAnalysis('P-C', 'Spearman')
        rho_kc, p_value_kc = SA.correlationAnalysis('K-C', 'Spearman')

        result_data = {
            "pearson_pc": correlation_pc,
            "pearson_kc": correlation_kc,
            "srho_pc": rho_pc,
            "svalue_pc": p_value_pc,
            "srho_kc": rho_kc,
            "svalue_kc": p_value_kc
        }

        # 返回成功响应和额外数据
        return jsonify({
            'message': 'scatter.html generated successfully',
            'data': result_data
        }), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 打印错误信息
        return jsonify({'error': '生成 scatter.html 时出错'}), 500  # 不泄露具体错误信息


@app.route('/encrypt', methods=['POST'])
def encrypt():
    encoding_type = request.form.get('n1')
    message = request.form.get('message')
    key = request.form.get('key')

    # 检查输入是否为空
    if not message or not key:
        return jsonify(error="Message and key cannot be empty."), 400

    print(f"Encoding Type: {encoding_type}, Message: {message}, Key: {key}")  # Debugging line

    sdes = SDES()

    if encoding_type == 'bit':
        message = np.array(list(map(int, message)), dtype=np.uint8)
        key = np.array(list(map(int, key)), dtype=np.uint8)

        if len(message) != 8 or len(key) != 10:
            return jsonify(error="Invalid message or key length."), 400

        encrypted_message = sdes.encryptOrDecrypt(message, key, 'E')
        encrypted_message = encrypted_message.tolist()  # Convert to list
    else:
        key = np.array(list(map(int, key)), dtype=np.uint8)
        encrypted_message = sdes.encryptString(message, key)

    print(f"Encrypted Message: {encrypted_message}")  # Debugging line
    return jsonify(result=encrypted_message)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    encoding_type = request.form.get('n1')
    message = request.form.get('message')
    key = request.form.get('key')

    # 检查输入是否为空
    if not message or not key:
        return jsonify(error="Message and key cannot be empty."), 400

    print(f"Encoding Type: {encoding_type}, Message: {message}, Key: {key}")  # Debugging line

    sdes = SDES()

    if encoding_type == 'bit':
        message = np.array(list(map(int, message)), dtype=np.uint8)
        key = np.array(list(map(int, key)), dtype=np.uint8)

        if len(message) != 8 or len(key) != 10:
            return jsonify(error="Invalid message or key length."), 400

        decrypted_message = sdes.encryptOrDecrypt(message, key, 'D')
        decrypted_message = decrypted_message.tolist()  # Convert to list
    else:
        key = np.array(list(map(int, key)), dtype=np.uint8)
        decrypted_message = sdes.decryptString(message, key)

    print(f"Decrypted Message: {decrypted_message}")  # Debugging line
    return jsonify(result=decrypted_message)


@app.route('/bruteForce', methods=['POST'])
def bruteForce():

    message_plain = request.form.get('message_plain')
    message_cipher = request.form.get('message_cipher')
    # 检查输入是否为空
    if not message_plain or not message_cipher:
        return jsonify(error="Message and key cannot be empty."), 400

    print(f" Message Plain: {message_plain}, Message Cipher: {message_cipher}")  # Debugging line
    
    SA = StatisticalAnalysis()
    message_plain = np.array(list(map(int, message_plain)), dtype=np.uint8)
    message_cipher = np.array(list(map(int, message_cipher)), dtype=np.uint8)

    time_taken, key = SA.bruteForceAttack(message_plain, message_cipher)
    key = [k.tolist() if isinstance(k, np.ndarray) else k for k in key]  # Convert numpy arrays to lists
    return jsonify(time=time_taken,key=key)


if __name__ == '__main__':
    app.run(debug=True)
