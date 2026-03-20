import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 从环境变量读取 GitHub Token
api_key = os.getenv("GITHUB_TOKEN")

# GitHub Models 的配置（不用改）
GITHUB_MODELS_API_URL = "https://models.inference.ai.azure.com/chat/completions"
GITHUB_MODELS_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 🔥 改用 Mistral 模型（这个名字是官方标准的，肯定能用）
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # 检查 Key 是否存在
    if not api_key:
        return jsonify({"error": "服务器没配置 GitHub Token"}), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400
        
        # 初始化客户端（使用 GitHub 的地址）
        client = OpenAI(
            api_key=api_key,
            base_url=GITHUB_MODELS_API_URL,
            default_headers=GITHUB_MODELS_HEADERS
        )
        
        # 调用 API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个乐于助人的AI助手，请用中文回答。"},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_reply = response.choices[0].message.content
        return jsonify({"reply": ai_reply})
    
    except Exception as e:
        # 打印详细错误到日志，方便排查
        print(f"错误详情: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
