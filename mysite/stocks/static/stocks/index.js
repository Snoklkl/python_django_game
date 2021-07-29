 /*
  function switchChart() {
    if(actions_left > 0) {
      actions_left = actions_left - 1;
    }   
    else if(actions_left == 0) {
      actions_left = 5;
      switch([current_time_int]) {
        case 1:

          break;
        case 2:

          break;

        case 3:

          break;

        case 4:

          break;

        case 5:

          break;

        case 6:

          break;

        case 7:

          break;

        case 8:

          break;

        case 9:

          break;

        case 10:

          break;

        case 11:

          break;
        case 12:

          break;
    }
    }


  };
 */
  import { Chart, LineController, LineElement, PointElement, LinearScale, Title } from `chart.js`


 
var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: {{ array_}},
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


  