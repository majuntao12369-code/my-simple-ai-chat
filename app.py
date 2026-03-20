import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# 关键：从环境变量读取Key
api_key = os.getenv("OPENAI_API_KEY")
print(f"【启动时检查】API Key 的前5位是: {api_key[:5] if api_key else '没有Key'}")

@app.route('/')
def index():
    print("【访问日志】有人打开了首页")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    print("=" * 50)
    print("【收到聊天请求】")
    
    # 1. 检查Key是否存在
    if not api_key:
        print("❌ 错误：API Key 没设置！")
        return jsonify({"error": "服务器没配置API Key"}), 500
    
    try:
        # 2. 获取前端数据
        data = request.get_json()
        print(f"收到的数据: {data}")
        
        user_message = data.get('message')
        if not user_message:
            print("❌ 错误：消息为空")
            return jsonify({"error": "消息不能为空"}), 400
        
        print(f"用户说: {user_message}")
        
        # 3. 调用OpenAI
        client = OpenAI(api_key=api_key)
        print("正在调用OpenAI API...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个乐于助人的AI助手，请用中文回答。"},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_reply = response.choices[0].message.content
        print(f"✅ AI回复: {ai_reply[:50]}...")  # 只打印前50字
        print("=" * 50)
        
        return jsonify({"reply": ai_reply})
    
    except Exception as e:
        # 🔥 关键：打印完整错误信息到Render日志
        print(f"❌ 发生错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印完整堆栈
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
