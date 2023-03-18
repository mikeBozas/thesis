    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["1-2018", "2-2018", "3-2018", "4-2018", "5-2018"],
            datasets: [{
                    label: 'Employee 1',
                    data: [50, 80, 30, 55, 20],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.2)',
                    ]
                },
                {
                label: 'Employee 2',
                    data: [40, 97, 20, 65, 30],
                    backgroundColor: [
                        'rgba(54, 50, 235, 0.2)',
                    ]
                }
            ]   
        },
        options: {
            elements:{
                line: {
                    tension : 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        max: 100
                    },
                }]
            }
        }
    });
