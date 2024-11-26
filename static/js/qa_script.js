// qa_script.js
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

// 用户头像与机器人头像的路径，从静态资源目录加载
const userAvatar = "./static/images/user.jpg";
const botAvatar = "./static/images/bot.jpg";

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // 显示用户消息
    const userMessage = document.createElement("div");
    userMessage.textContent = message;
    userMessage.className = "message user-message";

    // 创建用户头像
    const userImage = document.createElement("img");
    userImage.src = userAvatar;
    userImage.className = "avatar";

    // 将用户头像和消息一起放到 message-container 中
    const userMessageContainer = document.createElement("div");
    userMessageContainer.className = "message-container message-container-right";
    userMessageContainer.appendChild(userImage);
    userMessageContainer.appendChild(userMessage);
    chatBox.appendChild(userMessageContainer);
    chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最底部

    userInput.value = ""; // 清空输入框

    // 发送问题到后端
    try {
        const response = await fetch("/rag/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 显示机器人回复
        const botMessage = document.createElement("div");
        botMessage.textContent = data.answer || "No answer available.";
        botMessage.className = "message bot-message";

        // 创建机器人头像
        const botImage = document.createElement("img");
        botImage.src = botAvatar;
        botImage.className = "avatar";

        // 将机器人头像和消息一起放到 message-container 中
        const botMessageContainer = document.createElement("div");
        botMessageContainer.className = "message-container";
        botMessageContainer.appendChild(botImage);
        botMessageContainer.appendChild(botMessage);
        chatBox.appendChild(botMessageContainer);
        chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最底部
    } catch (error) {
        console.error("Error:", error);

        const botMessage = document.createElement("div");
        botMessage.textContent = "An error occurred. Please try again.";
        botMessage.className = "message bot-message";

        // 创建机器人头像
        const botImage = document.createElement("img");
        botImage.src = botAvatar;
        botImage.className = "avatar";

        // 将头像和消息内容添加到消息容器
        const botMessageContainer = document.createElement("div");
        botMessageContainer.className = "message-container";
        botMessageContainer.appendChild(botImage);
        botMessageContainer.appendChild(botMessage);
        chatBox.appendChild(botMessageContainer);
        chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最底部
    }
}

// 点击发送按钮时发送消息
sendButton.addEventListener("click", sendMessage);

// 按下 Enter 键发送消息
userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});
