import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# 加载环境变量
app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")

# 启动时打印Key的前5位，方便确认
if api_key:
    print(f"【启动时检查】API Key 的前5位是: {api_key[:5]}")
else:
    print("❌ 【启动时检查】没找到API Key！请去Render设置环境变量！")

# 初始化客户端（全局只初始化一次）
try:
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI 客户端初始化成功")
except Exception as e:
    print(f"❌ OpenAI 初始化失败: {e}")
    client = None

@app.route('/')
def index():
    print("【访问日志】有人打开了首页")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    print("=" * 30)
    print("【收到聊天请求】")
    
    # 1. 检查Key
    if not api_key:
        print("❌ 错误：API Key 没设置！")
        return jsonify({"error": "服务器没配置API Key"}), 500
    
    # 2. 检查客户端
    if not client:
        print("❌ 错误：OpenAI客户端初始化失败！")
        return jsonify({"error": "OpenAI客户端初始化失败"}), 500

    try:
        # 3. 获取数据
        data = request.get_json()
        print(f"收到的数据: {data}")
        
        user_message = data.get('message')
        if not user_message:
            print("❌ 错误：消息为空")
            return jsonify({"error": "消息不能为空"}), 400
        
        print(f"用户说: {user_message}")
        
        # 4. 调用OpenAI（关键步骤）
        print("正在调用OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个乐于助人的AI助手，请用中文回答。"},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_reply = response.choices[0].message.content
        print(f"✅ AI回复成功: {ai_reply[:30]}...")
        print("=" * 30)
        
        return jsonify({"reply": ai_reply})
    
    except Exception as e:
        # 🔥 关键修改：把完整的错误堆栈打印出来
        print(f"❌ 发生错误: {type(e).__name__}")
        print(f"❌ 错误详情: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

if __name__ == '__main__':
    # Render会通过环境变量PORT指定端口
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 服务器启动在端口 {port}")
    app.run(host='0.0.0.0', port=port)
