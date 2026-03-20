import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 🔥 关键修改：从环境变量读取 GitHub Token
api_key = os.getenv("GITHUB_TOKEN")

# GitHub Models 的配置
GITHUB_MODELS_API_URL = "https://models.inference.ai.azure.com/chat/completions"
GITHUB_MODELS_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 支持的模型列表（GitHub Models 免费提供）
# 你可以换成其他模型，比如 "meta-llama/Meta-Llama-3-8B-Instruct"
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400
        
        # 🔥 关键：调用 GitHub Models API（格式和OpenAI几乎一样）
        client = OpenAI(
            api_key=api_key,
            base_url=GITHUB_MODELS_API_URL,
            default_headers=GITHUB_MODELS_HEADERS
        )
        
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
        print(f"错误: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
