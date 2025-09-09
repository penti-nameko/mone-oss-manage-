// ダッシュボード統計グラフ（Chart.js利用想定）
function renderStatsChart(data) {
    // Chart.js等でグラフ描画
    // 例: new Chart(ctx, {...})
}

// テーブルフィルタ
function filterTable(inputId, tableId) {
    const filter = document.getElementById(inputId).value.toLowerCase();
    const rows = document.getElementById(tableId).getElementsByTagName('tr');
    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = rows[i].innerText.toLowerCase().includes(filter) ? '' : 'none';
    }
}