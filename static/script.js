document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const sendMessage = async () => {
        const text = userInput.value.trim();
        if (!text) return;

        // 显示用户消息
        addMessage(text, 'user-message');
        userInput.value = '';
        
        // 显示"思考中"
        const thinkingMsg = addMessage("AI 正在思考...", 'ai-message', true);

        try {
            console.log("📤 发送请求到 /chat");
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            // 移除"思考中"
            chatBox.removeChild(thinkingMsg);

            console.log("📥 收到响应，状态:", res.status);

            if (!res.ok) {
                // 如果状态码不是200，抛出错误
                const errText = await res.text();
                throw new Error(`HTTP ${res.status}: ${errText}`);
            }

            const data = await res.json();
            console.log("解析数据:", data);

            if (data.reply) {
                addMessage(data.reply, 'ai-message');
            } else {
                // 🔥 显示后端返回的具体错误！
                addMessage(`❌ 错误: ${data.error}`, 'ai-message');
            }

        } catch (err) {
            console.error('捕获到前端错误:', err);
            if (chatBox.contains(thinkingMsg)) {
                chatBox.removeChild(thinkingMsg);
            }
            // 显示具体的错误信息
            addMessage(`❌ 连接失败: ${err.message}`, 'ai-message');
        }
    };

    const addMessage = (text, className, isThinking = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);
        if (isThinking) {
            messageDiv.style.fontStyle = 'italic';
            messageDiv.id = 'thinking-indicator';
        }
        
        const messageP = document.createElement('p');
        messageP.textContent = text;
        messageDiv.appendChild(messageP);
        
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageDiv;
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
