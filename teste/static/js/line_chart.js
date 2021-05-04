var ctx = document.getElementById("myChart");

var stars = [135850, 52122, 148825, 16939, 9763];
var frameworks = ["React", "Angular", "Vue", "Hyperapp", "Omi"];

var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: frameworks,
    datasets: [
      {
        label: "Github Stars",
        data: stars,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1
      }
    ]
  }
});