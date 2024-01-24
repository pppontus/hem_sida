// Function to fetch JSON data
async function fetchData() {
    const response = await fetch('daylight_data.json');  // Adjust the path to your JSON file if necessary
    const data = await response.json();
    return data;
}

// Function to create the chart
function createChart(data) {
    const ctx = document.getElementById('daylightChart').getContext('2d');

    // Get today's date in the same format as your data
    const today = new Date().toISOString().split('T')[0];

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.Date),
            datasets: [{
                label: 'Dagljus Timmar',  // Daylight Hours
                data: data.map(item => item.DaylightHours),
                borderColor: '#1E90FF',  // DodgerBlue color
                backgroundColor: 'rgba(30, 144, 255, 0.2)',  // Translucent blue
                fill: true,
                tension: 0.3  // Adds some curve to the line
            }, {
                label: 'Dagsljusförändring (minuter)',  // Daylight Change (minutes)
                data: data.map(item => item.DaylightChange),
                borderColor: '#FFD700',  // Gold color
                backgroundColor: 'rgba(255, 215, 0, 0.2)',  // Translucent gold
                fill: true,
                tension: 0.3  // Adds some curve to the line
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'category',
                    labels: data.map(item => item.Date)
                },
                yHours: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Timmar'  // Hours
                    }
                },
                yChange: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Minuter',  // Minutes
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        lineToday: {
                            type: 'line',
                            xMin: today,
                            xMax: today,
                            borderColor: '#A9A9A9',
                            borderWidth: 2,
                            label: {
                                content: today,  // Today
                                enabled: true,
                                position: 'top'
                            }
                        }
                    }
                }
            }
        }
    });
}


// Main function to fetch data and create chart
async function main() {
    const data = await fetchData();
    createChart(data);
}

main();  // Run the main function
