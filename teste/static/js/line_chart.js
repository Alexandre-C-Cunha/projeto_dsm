var ctx = document.getElementById("lineChart");

var stars = [135850, 52122, 148825, 16939, 9763, 170000];
var frameworks = ["1970", "1980", "1990", "2000", "2010","2020"];

var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: frameworks,
    datasets: [
      {
        label: "CFEM",
        data: stars,
        borderColor: "rgba(0, 189, 47, 1)",
        borderWidth: 2,
        color: "rgba(0, 189, 47, 1)",
      }
    ]
  },
  options: {
      plugins: {
    datalabels: {
        color: "white",
        font: {
              weight: 'bold',
              size: 14,
            },
    },
},
       legend: {
        },
      title: {
            display: true,
            fontColor: 'white',
            text: 'CFEM (1970-2021)'
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:false,
                    fontColor: 'gray'
                },
            }],
          xAxes: [{
                ticks: {
                    stepSize: 100,
                    fontColor: 'gray'
                },
            }]
        } 
        
    }
});