document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const sendMessage = async () => {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, 'user-message');
        userInput.value = '';
        
        const thinkingMsg = addMessage("AI思考中...", 'ai-message', true);

        try {
            console.log("准备发送请求到 /chat");
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            
            console.log("收到响应，状态码:", res.status);

            chatBox.removeChild(thinkingMsg);

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }

            const data = await res.json();
            console.log("解析后的数据:", data);

            if (data.reply) {
                addMessage(data.reply, 'ai-message');
            } else {
                // 🔥 显示后端返回的具体错误
                addMessage(`错误: ${data.error}`, 'ai-message');
            }

        } catch (err) {
            console.error('捕获到错误:', err);
            chatBox.removeChild(thinkingMsg);
            addMessage(`连接失败: ${err.message}`, 'ai-message');
        }
    };

    const addMessage = (text, cls, isThinking = false) => {
        const div = document.createElement('div');
        div.className = `message ${cls}`;
        if(isThinking) { 
            div.style.fontStyle = 'italic'; 
            div.id = 'thinking'; 
        }
        div.innerHTML = `<p>${text}</p>`;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
        return div;
    };

    sendBtn.onclick = sendMessage;
    userInput.onkeypress = (e) => e.key === 'Enter' && sendMessage();
});

