document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // 发送消息的函数
    const sendMessage = async () => {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        // 1. 在聊天框显示用户消息
        addMessage(messageText, 'user-message');
        userInput.value = '';
        
        // 显示“正在输入...”提示
        const thinkingMessage = addMessage("AI 正在思考...", 'ai-message', true);

        try {
            // 2. 发送消息到后端
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) throw new Error('网络响应错误');

            const data = await response.json();
            
            // 移除“正在输入...”提示
            chatBox.removeChild(thinkingMessage);

            // 3. 在聊天框显示AI回复
            if (data.reply) {
                addMessage(data.reply, 'ai-message');
            } else {
                addMessage('抱歉，我好像出错了。', 'ai-message');
            }

        } catch (error) {
            console.error('Error:', error);
            chatBox.removeChild(thinkingMessage); // 出错也要移除提示
            addMessage('抱歉，连接服务器失败。', 'ai-message');
        }
    };

    // 将消息添加到聊天框的函数
    const addMessage = (text, className, isThinking = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);
        if (isThinking) {
            messageDiv.style.fontStyle = 'italic';
            messageDiv.id = 'thinking-indicator'; // 给个id方便找到并删除
        }
        
        const messageP = document.createElement('p');
        messageP.textContent = text;
        messageDiv.appendChild(messageP);
        
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到底部
        return messageDiv; // 返回创建的元素，方便之后删除
    };

    // 绑定事件
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
