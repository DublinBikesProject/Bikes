		var myVar;

		function myFunctionL() {
		    myVar = setTimeout(showPage, 3000);
		}

		function showPage() {
		    document.getElementById("overlay").style.display = "none";
		    document.getElementById("myDiv").style.display = "block";
		}
        
        /* Set the width of the side navigation to 250px */
        document.getElementById("sidebar").addEventListener('click', openNav);
function openNav() {
    document.getElementById("sidebar").style.width = "80px";
    
}

    
 document.getElementById("sidebar").addEventListener('click', closeNav);  
function closeNav() {
    document.getElementById("sidebar").style.width = "0";
}

		var slat;
		var slng;
		var y = [];
		var options = JSON.parse('{{ data | tojson | safe }}');

		$('#Input').append('<option selected="selected" disabled="disabled">Select a station</option>')

		for (var i = 0; i < options.length; i++) {
		    $('#Input').append('<option value="' + String(options[i].address) + '">' + String(options[i].address) + '</option>');
		    y.push(options[i]);
		}

		function myFunction() {
		    var x = document.getElementById("Input").value;

		    for (var i = 0; i < options.length; i++) {
		        if (y[i].address == x) {

		            if (y[i].banking == '0') {
		                x = 'No';
		            } else if (y[i].banking == '1') {
		                x = "Yes";
		            }

		            loclat = y[i].lat;
		            loclng = y[i].lng;

		            document.getElementById("test").addEventListener('click', showDetails(), false);

		        }

		        function showDetails() {
		            var popup = document.createElement('div');
		            popup.className = 'popup';
		            popup.id = 'test';
		            var cancel = document.createElement('div');
		            cancel.className = 'cancel';
		            cancel.innerHTML = 'X';
		            cancel.onclick = function(e) {
		                popup.parentNode.removeChild(popup)
		            };
		            var message = document.createElement('span');
		            message.innerHTML = "<b>You selected: </b>" + y[i].address + "<br>" + "<b>Available Bikes:</b> " + " " + y[i].available_bikes + "<br> " + "<b>Available Bike Stands:</b> " + y[i].available_bike_stands + " <br>" + "<b>The stop is: </b>" + y[i].status + "<br>" + "<b>Banking Available: </b>" + x + "<br>";
		            popup.appendChild(message);
		            popup.appendChild(cancel);
		            document.body.appendChild(popup);

		        }
		    }
		}

		var weatherData = JSON.parse('{{ weather | tojson | safe }}');
		var temp = weatherData[0].temp;
		var icon = weatherData[0].icon;
        var pressure = weatherData[0].pressure;
        var humidity = weatherData[0].humidity;
        var minTemp = weatherData[0].temp_min;
        var maxTemp = weatherData[0].temp_max;
        var windspeed = weatherData[0].windspeed; 

		var weatherWidget = "<div id='weatherWidget'>";
		weatherWidget += "<span id='temperature'>" + Math.round(temp) + "°</span>" + "<img src=../static/" + icon + ".png id='icons'/>";
		document.getElementById('weather').innerHTML = weatherWidget;
        var extra = document.getElementById("extraWeather");
        
        
        function displayWeather() {
                    if (extra.style.display === "none") {
                        extra.style.display = "block";
                        extra.innerHTML = "Pressure: " + pressure + "<br>Humidity: " + humidity + "<br>Minimum Temperature: " + minTemp + "°C, <br>Maximum Temperature: " + maxTemp + "°C, <br>Windspeed" + windspeed;
                } else {
                    extra.style.display = "none";
                }
        
            
        }

		    // from https://stackoverflow.com/questions/28415178/how-do-you-show-the-current-time-on-a-web-page

		//(function() {
		  //  var clockElement = document.getElementById("clock");

//		    function updateClock(clock) {
//		        clock.innerHTML = new Date().toLocaleTimeString();
//		    }

//		    setInterval(function() {
//		        updateClock(clockElement);
//		    }, 1000);

//		}());

		function initMap() {
		    directionsService = new google.maps.DirectionsService();
		    directionsDisplay = new google.maps.DirectionsRenderer();
			
			
			var myStyles =[{
        		featureType: "poi",
        		elementType: "labels",
        		stylers: [
              		{ visibility: "off" }
				]
    		}];
			
		    var map = new google.maps.Map(document.getElementById('map'), {
		        center: new google.maps.LatLng(53.3450, -6.2603),
		        zoom: 14,
		        mapTypeId: 'roadmap',
				styles: myStyles 

		    });

		    var points = JSON.parse('{{ data | tojson | safe }}');
		    var marker;
		    var current;
		    var infoWindow;
		    var available = points.available_bike_stands;
		    infoWindow = new google.maps.InfoWindow;
		    infoBikes = new google.maps.InfoWindow;


		    var icon = {
		        url: '../static/marker.png', // url
		        scaledSize: new google.maps.Size(30, 50), // scaled size

		    };

		    var bikeicon = {
		        url: '../static/bike_marker.png', // url
		        scaledSize: new google.maps.Size(40, 40), // scaled size            
		    };

		    var markers = [];
		    for (var i = 0; i < points.length; i++) {

		        var capacity = points[i].available_bikes + points[i].available_bike_stands;

		        var image_url;
		        //console.log(points[i].available_bikes)
		        if (points[i].available_bikes <= (capacity * 0.20)) {
		            image_url = "../static/bike_marker_full.png";
		        } else if (points[i].available_bikes <= (capacity * 0.6)) {
		            image_url = '../static/bike_marker_middle.png';
		        } else {
		            image_url = '../static/bike_marker_free.png';
		        }

		        var bikeicon = {
		            url: image_url, // url
		            scaledSize: new google.maps.Size(40, 40), // scaled size            
		        };

		        marker = new google.maps.Marker({
		            position: new google.maps.LatLng(points[i].lat, points[i].lng),
		            map: map,
		            animation: google.maps.Animation.DROP,
		            icon: bikeicon,
		            title: points[i].address

		        });
		        markers.push(marker);
				
				current = new google.maps.Marker({
		                position: new google.maps.LatLng(53.3450, -6.2603),
		                map: map,
		                animation: google.maps.Animation.DROP,
		                icon: icon,
		                title: 'Me'
		            });

		        google.maps.event.addListener(marker, 'click', (function(marker, i) {
		            return function() {

		                infoBikes.open(map, this);
		                infoBikes.setContent("Station name: " + points[i].address + "<br>Available bikes: " + points[i].available_bikes + "<br>Empty stands: " + points[i].available_bike_stands);

		            }

		        })(marker, i));

		        google.maps.event.addListener(marker, 'dblclick', (function(marker, i) {
		            return function() {
		                directionsService.route({

		                    origin: current.position,
		                    //destination: new google.maps.LatLng(53.3488,-6.28164),
		                    destination: new google.maps.LatLng(marker.getPosition().lat(), marker.getPosition().lng()),
		                    //destination: new google.maps.LatLng(points[i].lat, points[i].lng), 
		                    travelMode: 'WALKING'
		                }, function(response, status) {
		                    if (status === 'OK') {
		                        directionsDisplay.setDirections(response);
		                    } else {
		                        window.alert('Directions request failed due to ' + status);
		                    }
		                });
		            }
		        })(marker, i));

		        google.maps.event.addDomListener(document.getElementById('Input'), 'change', (function(marker, i) {
		            return function() {

		                var newX = document.getElementById("Input").value;

		                for (var k = 0; k < points.length; k++) {
		                    if (y[k].address == newX) {
		                        slat = y[k].lat;
		                        slng = y[k].lng;
		                    }
		                }
		                console.log(marker.position.lat() + " " + marker.position.lng());

		                for (var i = 0; i < markers.length; i++) {
		                    var a = marker.position.lng();
		                    var b = slng;
		                    var diff = Math.abs(a - b);

		                    if (marker.position.lat() == slat && diff < 0.00001) {
		                        marker.setAnimation(google.maps.Animation.BOUNCE);
		                        setTimeout(function() {
		                            marker.setAnimation(null);
		                        }, 1400);
		                    }
		                }
		            }
		        })(marker, i));
		    }

		    directionsDisplay.setMap(map);
		}
	
	  
      google.charts.load('current', {
    'packages': ['corechart']
});
//google.charts.setOnLoadCallback(drawVisualization);

function drawVisualization() {
    //The path is populated by the select which is the station
    //This generates the flask query and creates the URL that holds the data
    $.getJSON( '/daily/'+document.getElementById("Input").value, function( daily ) {
        
        console.log(daily);
 
            //to access the data need to delve one level deeper by access the name of the array created in the flask query.
            var DATA = google.visualization.arrayToDataTable([
                ['Time of Day (Hourly)', 'Available Bikes', 'Available Bike Stands', 'mm rain'],
                ['Monday', daily.data[2].ab, daily.data[2].ast, daily.data[9].r],
                ['Tuesday', daily.data[6].ab, daily.data[6].ast, daily.data[13].r],
                ['Wednesday', daily.data[7].ab, daily.data[7].ast, daily.data[14].r],
                ['Thursday', daily.data[5].ab, daily.data[5].ast, daily.data[12].r],
                ['Friday', daily.data[1].ab, daily.data[1].ast, daily.data[8].r],
                ['Saturday', daily.data[3].ab, daily.data[3].ast, daily.data[10].r],
                ['Sunday', daily.data[4].ab, daily.data[4].ast, daily.data[11].r],
            ]);
 
    
   var options = {
                width: 575,
                height: 345,
                colors: ['#008080', '#707ac2', "#7ac270"],
                backgroundColor: '#e6e6e6',
                chartArea: {'width': '73%'},
      title : document.getElementById("Input").value, 
        legend: {position: 'in'},
	  vAxis: {title: 'Daily Avg Station Data '},	
      hAxis: {title: 'Day'},
      seriesType: 'bars',
      series: {2: {type: 'line'}}
    };
	  
           
            var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
    chart.draw(DATA, options);
		 
    }
        
        );
}

   
 function drawVisualisation2(x) {
    
    
           //The path is populated by the select which is the station
    //This generates the flask query and creates the URL that holds the data  
    
    $.getJSON( "/daily/"+document.getElementById("Input").value+'/'+document.getElementById("day").value, function( daily ) {
        
        console.log(daily);          

            var DATA = google.visualization.arrayToDataTable([
                ['Time of Day (Hourly)', 'Available Bikes', 'Available Bike Stands', 'mm rain'],
                ['06:00', daily.Hourly[6].ab, daily.Hourly[6].ast, daily.Hourly[24].r],
                ['07:00', daily.Hourly[7].ab, daily.Hourly[7].ast, daily.Hourly[25].r],
                ['08:00', daily.Hourly[8].ab, daily.Hourly[8].ast, daily.Hourly[26].r],
                ['09:00', daily.Hourly[9].ab, daily.Hourly[9].ast, daily.Hourly[27].r],
                ['10:00', daily.Hourly[10].ab, daily.Hourly[10].ast, daily.Hourly[28].r],
                ['11:00', daily.Hourly[11].ab, daily.Hourly[11].ast, daily.Hourly[29].r],
                ['12:00', daily.Hourly[12].ab, daily.Hourly[12].ast, daily.Hourly[30].r],
                ['13:00', daily.Hourly[13].ab, daily.Hourly[13].ast, daily.Hourly[31].r],
                ['14:00', daily.Hourly[14].ab, daily.Hourly[14].ast, daily.Hourly[32].r],
                ['15:00', daily.Hourly[15].ab, daily.Hourly[15].ast, daily.Hourly[33].r],
                ['16:00', daily.Hourly[16].ab, daily.Hourly[16].ast, daily.Hourly[34].r],
                ['17:00', daily.Hourly[17].ab, daily.Hourly[17].ast, daily.Hourly[35].r],
                ['18:00', daily.Hourly[18].ab, daily.Hourly[18].ast, daily.Hourly[36].r],
                ['19:00', daily.Hourly[19].ab, daily.Hourly[19].ast, daily.Hourly[37].r],
                ['20:00', daily.Hourly[20].ab, daily.Hourly[20].ast, daily.Hourly[38].r],
                ['21:00', daily.Hourly[21].ab, daily.Hourly[21].ast, daily.Hourly[39].r],
                ['22:00', daily.Hourly[22].ab, daily.Hourly[22].ast, daily.Hourly[40].r],
                ['23:00', daily.Hourly[23].ab, daily.Hourly[23].ast, daily.Hourly[41].r], 
            ]);
 
   var options2 = {
                width: 720,
                height: 345,
                colors: ['#008080', '#707ac2', "#7ac270", "#7ac270"],
                backgroundColor: '#e6e6e6',
                chartArea: {'width': '73%'},
      title : document.getElementById("day").value, 
        legend: {position: 'in'},
	  vAxis: {title: 'Hourly Avg Station Data '},	
      hAxis: {title: 'Time'},
      seriesType: 'bars',
      series: {2: {type: 'line'}}
    };
	   //draw the chart in the approporate div element
            var chart = new google.visualization.ComboChart(document.getElementById('chart_div2'));
    chart.draw(DATA, options2);
		  	  
        }
    );
}  
		
		function prediction() {
    
    $.getJSON('/predict/'+document.getElementById("Input").value, function( daily ) {
        
       console.log(daily);
        document.getElementById("pred").innerHTML = "Predicted # of bikes <br> at this station in 3h: "+daily;
            }
    );
        
    }
		