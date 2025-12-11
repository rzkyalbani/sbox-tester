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

    // Create the radar chart
    window.radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Normalized Metrics Score',
                data: data,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(59, 130, 246, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
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
                    ticks: {
                        stepSize: 0.25,
                        callback: function(value) {
                            return (value * 100) + '%';
                        }
                    },
                    pointLabels: {
                        font: {
                            size: 12
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

    // Create a visualization showing SAC value with reference to the ideal value (0.5)
    // This will be a bar chart comparing actual vs ideal SAC
    const labels = ['SAC Value'];
    const actualSac = sacValue;
    const idealSac = 0.5;

    // Calculate the deviation from ideal
    const deviation = Math.abs(actualSac - idealSac);

    // Create the chart data
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Actual SAC Value',
                data: [actualSac],
                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            },
            {
                label: 'Ideal SAC Value',
                data: [idealSac],
                backgroundColor: 'rgba(107, 114, 128, 0.4)',
                borderColor: 'rgba(107, 114, 128, 1)',
                borderWidth: 1
            }
        ]
    };

    // Color based on how close to ideal the actual value is
    const backgroundColor = deviation < 0.05 ? 'rgba(34, 197, 94, 0.6)' : // green for close to ideal
                            deviation < 0.1 ? 'rgba(99, 102, 241, 0.6)' :  // blue for somewhat close
                            'rgba(239, 68, 68, 0.6)';                      // red for far from ideal

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
                },
                tooltip: {
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
                        callback: function(value) {
                            return value.toFixed(2);
                        }
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
    "Computing Nonlinearity (NL)…",
    "Analyzing Avalanche Effect (SAC)…",
    "Evaluating Bit Independence (BIC)…",
    "Measuring Differential Uniformity (DU)…",
    "Checking Linear Approximation Bias (LAP)…",
    "Assessing Algebraic Degree (AD)…",
    "Estimating Transparency Order (TO)…",
    "Finalizing Cryptographic Profile…"
];

// Educational messages with details
const educationalMessages = [
    "Computing Nonlinearity… higher NL increases resistance against linear attacks.",
    "Evaluating Avalanche Effect… ideal SAC is close to 0.5.",
    "Checking Bit Independence… ensuring output bits behave unpredictably.",
    "Analyzing Differential Uniformity… AES S-box uses DU = 4.",
    "Measuring Linear Approximation Probability… lower LAP = stronger cipher.",
    "Assessing Algebraic Degree… higher AD increases algebraic complexity.",
    "Estimating Transparency Order… impacts side-channel resistance.",
    "Finalizing cryptographic strength evaluation…"
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