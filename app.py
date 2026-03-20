import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量 (主要为本地测试准备)
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)

# 从环境变量中获取 OpenAI API Key
# 这是最安全的方式！Render会自动注入这个变量
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # 如果在Render上部署失败，这个错误信息会显示在日志里
    raise ValueError("OPENAI_API_KEY 环境变量未设置！请在Render后台配置。")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

# 定义首页路由，返回我们的聊天页面
@app.route('/')
def index():
    # render_template 会自动去 'templates' 文件夹里找 'index.html'
    return render_template('index.html')

# 定义聊天接口，前端会把消息发到这里
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 获取前端发送过来的JSON数据
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400

        # 调用 OpenAI Chat Completions API
        # 我们使用 gpt-3.5-turbo 模型，因为它便宜又快
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个乐于助人的AI助手，请用中文回答。"},
                {"role": "user", "content": user_message}
            ]
        )

        # 提取AI的回复
        ai_reply = response.choices[0].message.content

        # 以JSON格式返回AI的回复
        return jsonify({"reply": ai_reply})

    except Exception as e:
        # 打印详细错误到服务器日志，方便排查
        print(f"发生错误: {e}")
        return jsonify({"error": "服务器内部错误，请稍后再试。"}), 500

# 这部分是为了在本地测试时运行，Render会用gunicorn来启动，所以这部分在部署后不会执行
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
