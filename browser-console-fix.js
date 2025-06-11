// 浏览器控制台快速修复脚本
// 复制以下代码到浏览器控制台并按回车键执行

console.log('🔧 开始修复输入框文字显示问题...');

// 创建修复样式
const fixStyle = document.createElement('style');
fixStyle.id = 'input-text-fix';
fixStyle.innerHTML = `
/* 紧急输入框文字显示修复 */
.el-input__inner,
.el-input input,
input.el-input__inner,
.el-textarea__inner,
textarea.el-textarea__inner {
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.1) !important;
    -webkit-text-fill-color: #ffffff !important;
}

.el-input__inner::placeholder,
.el-textarea__inner::placeholder,
input::placeholder,
textarea::placeholder {
    color: rgba(255, 255, 255, 0.6) !important;
    -webkit-text-fill-color: rgba(255, 255, 255, 0.6) !important;
}

.el-input__wrapper,
.el-textarea__wrapper {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.el-input__wrapper.is-focus,
.el-input__wrapper:focus-within,
.el-textarea__wrapper.is-focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
}

/* 对话框内的特殊修复 */
.el-dialog .el-input__inner,
.el-dialog .el-textarea__inner,
.el-dialog input,
.el-dialog textarea {
    color: #ffffff !important;
    background: rgba(26, 26, 46, 0.8) !important;
    -webkit-text-fill-color: #ffffff !important;
}

.el-dialog .el-input__wrapper,
.el-dialog .el-textarea__wrapper {
    background: rgba(26, 26, 46, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* 全局输入框修复 */
input, textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* 针对 webkit 浏览器的自动填充修复 */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-text-fill-color: #ffffff !important;
    -webkit-box-shadow: 0 0 0 30px rgba(26, 26, 46, 0.8) inset !important;
    transition: background-color 5000s ease-in-out 0s !important;
}
`;

// 移除已存在的修复样式（如果有）
const existingFix = document.getElementById('input-text-fix');
if (existingFix) {
    existingFix.remove();
}

// 添加修复样式到页面
document.head.appendChild(fixStyle);

console.log('✅ 输入框文字显示修复已应用！');

// 强制刷新已存在的输入框样式
const inputs = document.querySelectorAll('input, textarea');
inputs.forEach(input => {
    // 强制重新渲染
    input.style.color = '#ffffff';
    input.style.webkitTextFillColor = '#ffffff';
    
    // 触发重绘
    const display = input.style.display;
    input.style.display = 'none';
    input.offsetHeight; // 触发重排
    input.style.display = display;
});

console.log(`🔄 已刷新 ${inputs.length} 个输入框的样式`);

// 测试函数
function testInputVisibility() {
    console.log('🧪 测试输入框可见性...');
    
    const testInputs = document.querySelectorAll('input[type="text"], textarea');
    testInputs.forEach((input, index) => {
        const computedStyle = window.getComputedStyle(input);
        const color = computedStyle.color;
        const backgroundColor = computedStyle.backgroundColor;
        const webkitTextFillColor = computedStyle.webkitTextFillColor;
        
        console.log(`输入框 ${index + 1}:`, {
            color,
            backgroundColor,
            webkitTextFillColor,
            element: input
        });
    });
}

// 监听新增的输入框
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    const newInputs = node.querySelectorAll ? node.querySelectorAll('input, textarea') : [];
                    newInputs.forEach(input => {
                        input.style.color = '#ffffff';
                        input.style.webkitTextFillColor = '#ffffff';
                    });
                }
            });
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

console.log('👀 已启动输入框监听器，新添加的输入框将自动修复');

// 暴露测试函数到全局
window.testInputVisibility = testInputVisibility;
window.fixInputDisplay = function() {
    console.log('🔧 重新应用输入框修复...');
    document.head.appendChild(fixStyle.cloneNode(true));
    
    const allInputs = document.querySelectorAll('input, textarea');
    allInputs.forEach(input => {
        input.style.color = '#ffffff';
        input.style.webkitTextFillColor = '#ffffff';
    });
    
    console.log('✅ 修复已重新应用！');
};

console.log('📚 可用命令:');
console.log('  testInputVisibility() - 测试输入框可见性');
console.log('  fixInputDisplay() - 重新应用修复');
console.log('');
console.log('💡 如果文字仍然不可见，请尝试：');
console.log('  1. 刷新页面后重新运行此脚本');
console.log('  2. 检查浏览器是否禁用了某些CSS属性');
console.log('  3. 尝试使用无痕模式');

// 自动测试
setTimeout(testInputVisibility, 1000); 