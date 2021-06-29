
  const newsApi = "94893aa1d959487f9c5b56e7d1919151";
  
   
  
  function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  } 
  
  
   $("#NewsButton").on("click", (function() {
      $.get("https://newsapi.org/v2/everything?q=abc&language=en&pageSize=2&from=2020-01-0`1&to=2020-01-31&apiKey=" + newsApi , (function(response){
           
           if(("#abcNews").length > 1) {
             $("#abcNews").empty()
           }
             
        for (var i=0; i < response.articles.length; i++){
        console.log(response.articles[i].title)
        var searchResponse = response.articles[i].title;
        $("#abcNews").append(searchResponse);
      

      }
         }))
   }))
      
   /*  
     switch([current_time_int]) {
        case 1:
         $.get("https://newsapi.org/v2/everything?q=abc&language=en&pageSize=2&from=2020-01-1&to=2020-01-31&q=abcd&apiKey=" + newsApi , (function(response){
           
           if(("#abcNews").length > 1) {
             $("#abcNews").empty()
           }
             
        for (var i=0; i < response.articles.length; i++){
        console.log(response.articles[i].title)
        var searchResponse = response.articles[i].title;
        $("#abcNews").append(searchResponse);
      

      }
         }))

         
         
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

   })
   )

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

  const labels = [
    'Dec (Last Year)',
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sept',
    'Oct',
    'Nov',
    'Dec',
  ];
  const data = {
    labels: labels,
    datasets: [{
      label: 'My First dataset',
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      data: [0, 10, 5, 2, 20, 30, 45],
    }]
  };

  const config = {
    type: 'line',
    data,
    options: {}
  };

    var myChart = new Chart(
      document.getElementById('myChart'),
      config
    );
  

     
