// 获取添加知识库按钮
const addKbButton = document.getElementById("create-knowledge");

// 监听添加知识库按钮的点击事件
addKbButton.addEventListener("click", () => {
    // 创建一个隐藏的文件输入框
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt,.pdf,.docx"; // 根据需求限制文件类型
    fileInput.style.display = "none";

    // 将文件输入框添加到页面
    document.body.appendChild(fileInput);

    // 监听文件选择事件
    fileInput.addEventListener("change", async () => {
        const file = fileInput.files[0]; // 获取用户选择的文件
        if (!file) {
            alert("请选择一个文件！");
            return;
        }

        const formData = new FormData();
        formData.append("file", file); // 将文件添加到 FormData 对象

        try {
            // 发起 POST 请求到 /rag/add/ 接口
            const response = await fetch("/rag/create/", {
                method: "POST",
                body: formData,
            });

            const result = await response.json(); // 解析响应数据
            if (response.ok) {
                alert(result.message || "文件上传并添加到知识库成功！");
            } else {
                alert(result.message || "上传失败，请重试！");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("上传操作失败，请检查后端服务！");
        } finally {
            // 从 DOM 中移除文件输入框
            document.body.removeChild(fileInput);
        }
    });

    // 模拟点击文件输入框，触发文件选择对话框
    fileInput.click();
});

// 监听清空知识库按钮
const clearKnowledge = async () => {
    try {
        const response = await fetch("/rag/clear/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                collection_name: "knowledge_collection",
                host: "localhost",
                port: 19530,
            }),
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error("Error clearing knowledge:", error);
        alert("Failed to clear knowledge.");
    }
};

document.getElementById("clear-knowledge").addEventListener("click", clearKnowledge);

