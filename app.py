'''
Author: Riceball chenlei9691@gmail.com
Date: 2024-07-03 23:01:09
LastEditors: Riceball chenlei9691@gmail.com
LastEditTime: 2024-07-04 00:44:21
FilePath: /home/Code/Her/app.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
import aiohttp
from aiohttp import web
from flask import Flask, jsonify
from HER import HER

app = Flask(__name__)

her = HER()

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, world!"})

@app.route('/async_route')
async def async_route():
    # 异步执行一些任务
    result = await async_task()
    return jsonify({"result": result})

@app.route('/chat', methods=['POST'])
async def chat():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response = chat_model.generate_response(prompt)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def async_task():
    # 这里可以添加异步任务，例如数据库查询、网络请求等
    return "Async task completed!"

if __name__ == '__main__':
    app.run(debug=True)