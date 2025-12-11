// Function to get chart theme based on current theme
function getChartTheme() {
    const isDarkMode = document.documentElement.classList.contains('dark');
    return isDarkMode ? 'dark' : 'light';
}

// Function to update charts when theme changes
function updateChartsTheme() {
    if (window.radarChartInstance) {
        // Update the radar chart with new theme
        const currentData = window.radarChartInstance.data;
        const chartOptions = window.radarChartInstance.options;

        // Update colors based on theme
        const chartTheme = getChartTheme();
        const textColor = chartTheme === 'dark' ? '#e5e7eb' : '#374151';
        const gridColor = chartTheme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
        const pointBackgroundColor = chartTheme === 'dark' ? 'rgba(255, 255, 255, 0.8)' : '#fff';
        const tooltipBgColor = chartTheme === 'dark' ? 'rgba(31, 41, 55, 0.9)' : 'rgba(255, 255, 255, 0.9)';
        const borderColor = chartTheme === 'dark' ? 'rgba(209, 213, 219, 0.3)' : 'rgba(209, 213, 219, 1)';

        // Update dataset colors
        currentData.datasets[0].backgroundColor = chartTheme === 'dark' ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)';
        currentData.datasets[0].borderColor = chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)';
        currentData.datasets[0].pointBackgroundColor = chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)';
        currentData.datasets[0].pointBorderColor = pointBackgroundColor;
        currentData.datasets[0].pointHoverBackgroundColor = pointBackgroundColor;
        currentData.datasets[0].pointHoverBorderColor = chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)';

        // Update options
        chartOptions.plugins.legend.labels.color = textColor;
        chartOptions.plugins.tooltip.backgroundColor = tooltipBgColor;
        chartOptions.plugins.tooltip.titleColor = textColor;
        chartOptions.plugins.tooltip.bodyColor = textColor;
        chartOptions.plugins.tooltip.borderColor = borderColor;
        chartOptions.scales.r.pointLabels.color = textColor;
        chartOptions.scales.r.ticks.color = textColor;
        chartOptions.scales.r.grid.color = gridColor;
        chartOptions.scales.r.angleLines.color = gridColor;

        window.radarChartInstance.update();
    }

    if (window.sacChartInstance) {
        // Update the SAC chart with new theme
        const currentData = window.sacChartInstance.data;
        const chartOptions = window.sacChartInstance.options;

        // Update colors based on theme
        const chartTheme = getChartTheme();
        const textColor = chartTheme === 'dark' ? '#e5e7eb' : '#374151';
        const gridColor = chartTheme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
        const tooltipBgColor = chartTheme === 'dark' ? 'rgba(31, 41, 55, 0.9)' : 'rgba(255, 255, 255, 0.9)';
        const borderColor = chartTheme === 'dark' ? 'rgba(209, 213, 219, 0.3)' : 'rgba(209, 213, 219, 1)';

        // Update dataset colors
        currentData.datasets[0].backgroundColor = chartTheme === 'dark' ? 'rgba(99, 102, 241, 0.6)' : 'rgba(59, 130, 246, 0.6)';
        currentData.datasets[0].borderColor = chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)';
        currentData.datasets[1].backgroundColor = chartTheme === 'dark' ? 'rgba(156, 163, 175, 0.4)' : 'rgba(107, 114, 128, 0.4)';
        currentData.datasets[1].borderColor = chartTheme === 'dark' ? 'rgba(156, 163, 175, 1)' : 'rgba(107, 114, 128, 1)';

        // Update options
        chartOptions.plugins.legend.labels.color = textColor;
        chartOptions.plugins.tooltip.backgroundColor = tooltipBgColor;
        chartOptions.plugins.tooltip.titleColor = textColor;
        chartOptions.plugins.tooltip.bodyColor = textColor;
        chartOptions.plugins.tooltip.borderColor = borderColor;
        chartOptions.scales.y.ticks.color = textColor;
        chartOptions.scales.y.grid.color = gridColor;
        chartOptions.scales.x.ticks.color = textColor;
        chartOptions.scales.x.grid.color = gridColor;

        window.sacChartInstance.update();
    }
}

// Function to render radar chart for normalized metrics
function renderRadarChart(metricsNormalized) {
    const ctx = document.getElementById('radarChart').getContext('2d');

    // Destroy existing chart if it exists
    if (window.radarChartInstance) {
        window.radarChartInstance.destroy();
    }

    // Prepare data for the radar chart
    const labels = Object.keys(metricsNormalized);
    const data = Object.values(metricsNormalized);

    // Get theme for chart colors
    const chartTheme = getChartTheme();
    const textColor = chartTheme === 'dark' ? '#e5e7eb' : '#374151'; // text-gray-200 or text-gray-700
    const gridColor = chartTheme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    const pointBackgroundColor = chartTheme === 'dark' ? 'rgba(255, 255, 255, 0.8)' : '#fff';

    // Create the radar chart
    window.radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Skor Metrik Ternormalisasi',
                data: data,
                backgroundColor: chartTheme === 'dark' ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)',
                borderColor: chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)',
                pointBorderColor: pointBackgroundColor,
                pointHoverBackgroundColor: pointBackgroundColor,
                pointHoverBorderColor: chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: textColor,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    backgroundColor: chartTheme === 'dark' ? 'rgba(31, 41, 55, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                    titleColor: textColor,
                    bodyColor: textColor,
                    borderColor: chartTheme === 'dark' ? 'rgba(209, 213, 219, 0.3)' : 'rgba(209, 213, 219, 1)',
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + (context.parsed.r * 100).toFixed(2) + '%';
                        }
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    grid: {
                        color: gridColor,
                    },
                    angleLines: {
                        color: gridColor,
                    },
                    pointLabels: {
                        color: textColor,
                        font: {
                            size: 12
                        }
                    },
                    ticks: {
                        stepSize: 0.25,
                        color: textColor,
                        callback: function(value) {
                            return (value * 100) + '%';
                        }
                    }
                }
            }
        }
    });
}

// Function to render SAC distribution chart
function renderSacChart(sacValue) {
    const ctx = document.getElementById('sacChart').getContext('2d');

    // Destroy existing chart if it exists
    if (window.sacChartInstance) {
        window.sacChartInstance.destroy();
    }

    // Get theme for chart colors
    const chartTheme = getChartTheme();
    const textColor = chartTheme === 'dark' ? '#e5e7eb' : '#374151'; // text-gray-200 or text-gray-700
    const gridColor = chartTheme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    const tooltipBgColor = chartTheme === 'dark' ? 'rgba(31, 41, 55, 0.9)' : 'rgba(255, 255, 255, 0.9)';
    const borderColor = chartTheme === 'dark' ? 'rgba(209, 213, 219, 0.3)' : 'rgba(209, 213, 219, 1)';

    // Create a visualization showing SAC value with reference to the ideal value (0.5)
    // This will be a bar chart comparing actual vs ideal SAC
    const labels = ['Distribusi SAC'];
    const actualSac = sacValue;
    const idealSac = 0.5;

    // Calculate the deviation from ideal
    const deviation = Math.abs(actualSac - idealSac);

    // Create the chart data
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Nilai SAC Aktual',
                data: [actualSac],
                backgroundColor: chartTheme === 'dark' ? 'rgba(99, 102, 241, 0.6)' : 'rgba(59, 130, 246, 0.6)',
                borderColor: chartTheme === 'dark' ? 'rgba(99, 102, 241, 1)' : 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            },
            {
                label: 'Nilai SAC Ideal',
                data: [idealSac],
                backgroundColor: chartTheme === 'dark' ? 'rgba(156, 163, 175, 0.4)' : 'rgba(107, 114, 128, 0.4)',
                borderColor: chartTheme === 'dark' ? 'rgba(156, 163, 175, 1)' : 'rgba(107, 114, 128, 1)',
                borderWidth: 1
            }
        ]
    };

    // Color based on how close to ideal the actual value is
    const backgroundColor = deviation < 0.05 ? (chartTheme === 'dark' ? 'rgba(34, 197, 94, 0.6)' : 'rgba(34, 197, 94, 0.6)') : // green for close to ideal
                            deviation < 0.1 ? (chartTheme === 'dark' ? 'rgba(99, 102, 241, 0.6)' : 'rgba(99, 102, 241, 0.6)') :  // blue for somewhat close
                            (chartTheme === 'dark' ? 'rgba(239, 68, 68, 0.6)' : 'rgba(239, 68, 68, 0.6)');                      // red for far from ideal

    // Update the first dataset's background color based on SAC quality
    data.datasets[0].backgroundColor = backgroundColor;

    window.sacChartInstance = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: textColor,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    backgroundColor: tooltipBgColor,
                    titleColor: textColor,
                    bodyColor: textColor,
                    borderColor: borderColor,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(4);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        color: textColor,
                        callback: function(value) {
                            return value.toFixed(2);
                        }
                    },
                    grid: {
                        color: gridColor,
                    }
                },
                x: {
                    ticks: {
                        color: textColor,
                    },
                    grid: {
                        color: gridColor,
                    }
                }
            }
        }
    });
}

// Initialize charts if metrics are already available (for page reloads)
document.addEventListener('DOMContentLoaded', function() {
    // Charts will be initialized when metrics are computed via displayResults function
});

// Educational Loading Message System
const loadingSteps = [
    "Menghitung Nonlinearitas (NL)…",
    "Menganalisis Efek Avalanche (SAC)…",
    "Mengevaluasi Kemandirian Bit (BIC)…",
    "Mengukur Uniformitas Diferensial (DU)…",
    "Memeriksa Bias Pendekatan Linear (LAP)…",
    "Menilai Derajat Aljabar (AD)…",
    "Memperkirakan Tingkat Transparansi (TO)…",
    "Menyelesaikan Profil Kriptografi…"
];

// Educational messages with details
const educationalMessages = [
    "Menghitung Nonlinearitas… NL yang lebih tinggi meningkatkan ketahanan terhadap serangan linear.",
    "Mengevaluasi Efek Avalanche… SAC ideal mendekati 0.5.",
    "Memeriksa Kemandirian Bit… memastikan bit output berperilaku tidak terduga.",
    "Menganalisis Uniformitas Diferensial… S-Box AES menggunakan DU = 4.",
    "Mengukur Probabilitas Pendekatan Linear… LAP yang lebih rendah = cipher yang lebih kuat.",
    "Menilai Derajat Aljabar… AD yang lebih tinggi meningkatkan kompleksitas aljabar.",
    "Memperkirakan Tingkat Transparansi… berdampak pada ketahanan terhadap serangan sisi saluran.",
    "Menyelesaikan evaluasi kekuatan kriptografi…"
];

// Function to start the message rotation
let messageInterval = null;

function startMessageRotation() {
    // If there's an existing interval, clear it
    if (messageInterval) {
        clearInterval(messageInterval);
    }

    let currentIndex = 0;

    // Update the loading message immediately
    updateLoadingMessage(currentIndex);
    currentIndex = (currentIndex + 1) % educationalMessages.length;

    // Set up the interval to rotate messages every 1200ms
    messageInterval = setInterval(() => {
        updateLoadingMessage(currentIndex);
        currentIndex = (currentIndex + 1) % educationalMessages.length;
    }, 1200);
}

function updateLoadingMessage(index) {
    const messageElement = document.getElementById('loadingMessage');
    if (messageElement) {
        messageElement.textContent = educationalMessages[index];
    }
}

// Store the function in the global window object so it can be called from index.html
window.startMessageRotation = startMessageRotation;