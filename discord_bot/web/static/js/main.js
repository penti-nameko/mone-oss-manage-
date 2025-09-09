// メニュー開閉
function toggleMenu() {
    const menu = document.getElementById('sidebar');
    menu.classList.toggle('active');
}

// 通知表示
function showNotification(msg, type='info') {
    const n = document.createElement('div');
    n.className = 'notification ' + type;
    n.innerText = msg;
    document.body.appendChild(n);
    setTimeout(() => n.remove(), 3000);
}