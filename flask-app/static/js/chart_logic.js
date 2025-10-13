// flask_app/static/js/chart_logic.js (VERSI DIPERBAIKI)

function drawRegressionChart(chartData) {
    // 1. Ambil konteks canvas
    const ctx = document.getElementById('regressionChart').getContext('2d');
    
    // 2. Konversi data Aktual ke format scatter plot
    const dataPoints = chartData.X_data.map((x, index) => ({
        x: x,
        // PERBAIKAN: Menggunakan nama variabel yang benar dari Python
        y: chartData.y_data_actual[index] 
    }));
    
    // 3. Konversi data Prediksi (Garis Regresi)
    const linePoints = chartData.X_data.map((x, index) => ({
        x: x,
        // PERBAIKAN: Menggunakan nama variabel yang benar dari Python
        y: chartData.y_data_predicted[index]
    }));

    // Opsional: Urutkan linePoints agar garisnya lurus, karena input X mungkin tidak terurut
    linePoints.sort((a, b) => a.x - b.x);


    new Chart(ctx, {
        type: 'scatter', 
        data: {
            datasets: [{
                label: 'Data Aktual',
                data: dataPoints,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                pointRadius: 5
            }, {
                label: 'Garis Regresi',
                data: linePoints,
                type: 'line', 
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                fill: false,
                tension: 0,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear', 
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Berat Kendaraan (kg)' // Disarankan menggunakan nama kolom aktual
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Konsumsi (Ltr/100km)' // Disarankan menggunakan nama kolom aktual
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Visualisasi Regresi Linear Matriks'
                }
            }
        }
    });
}