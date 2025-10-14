// flask_app/static/js/chart_logic.js (FIXED VERSION)

let regressionChartInstance = null; // simpan chart agar bisa di-destroy nanti

function drawRegressionChart(chartData) {
    // 1. Ambil konteks canvas
    const ctx = document.getElementById('regressionChart').getContext('2d');

    // 2. Hapus chart lama dulu kalau sudah ada
    if (regressionChartInstance) {
        regressionChartInstance.destroy();
    }

    // 3. Konversi data Aktual ke format scatter plot
    const dataPoints = chartData.X_data.map((x, index) => ({
        x: x,
        y: chartData.y_data_actual[index]
    }));

    // 4. Konversi data Prediksi (Garis Regresi)
    const linePoints = chartData.X_data.map((x, index) => ({
        x: x,
        y: chartData.y_data_predicted[index]
    })).sort((a, b) => a.x - b.x);

    // 5. Buat chart baru
    regressionChartInstance = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Data Aktual',
                    data: dataPoints,
                    backgroundColor: 'rgba(56, 189, 248, 0.7)', // biru lembut
                    borderColor: 'rgba(56, 189, 248, 1)',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointStyle: 'circle',
                },
                {
                    label: 'Garis Regresi',
                    data: linePoints,
                    type: 'line',
                    borderColor: 'rgba(249, 115, 22, 0.9)', // oranye terang
                    borderWidth: 3,
                    fill: false,
                    tension: 0.2,
                    pointRadius: 0,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: 20
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    grid: {
                        color: 'rgba(209, 213, 219, 0.3)',
                        borderDash: [5, 5]
                    },
                    title: {
                        display: true,
                        text: 'Berat Kendaraan (kg)',
                        font: { size: 14, weight: 'bold' },
                        color: '#374151'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(209, 213, 219, 0.3)',
                        borderDash: [5, 5]
                    },
                    title: {
                        display: true,
                        text: 'Konsumsi (Ltr/100km)',
                        font: { size: 14, weight: 'bold' },
                        color: '#374151'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Visualisasi Regresi Linear Matriks',
                    font: { size: 16, weight: 'bold' },
                    color: '#1f2937',
                    padding: { bottom: 20 }
                },
                legend: {
                    position: 'top',
                    labels: {
                        color: '#374151',
                        font: { size: 13 },
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(31, 41, 55, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#f9fafb',
                    padding: 10,
                    borderColor: '#60a5fa',
                    borderWidth: 1
                }
            }
        }
    });
}
