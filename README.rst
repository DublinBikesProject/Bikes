=====
Bikes
=====

This project is a web application that displays occupancy and weather information for Dublin Bikes. 


=============
Deliverables
=============


The link to the repository is as follows: https://github.com/DublinBikesProject/Bikes.git


========
Overview
========

The main features of this application are;

* We collected data from JCDecaux using an api link. 

* We stored the collected data in an Amazon RDS MYSQL instance.

* We created and maintained an EC2 instance used to run the web application. 

* We used the data to display bike station information on a map and the webpage. 

* We also collected weather data from an open weather map and displayed it in a weather widget. 



==================
Project Structure
==================

* The SRC folder contains test files, the scrapers and the predictive model for regression.

* The flask_app folder contains the necessary components to generate the web application interface. 
 

==============
Functionality
==============

* An on-click on the markers displays some occupancy information

* Dlovouble click provides directions to the station

* Collapsible side bar contains links to Dublin Bikes social media

* An on-click of the weather icon in the far left displays current weather information and future weather prediction.

* The select option in the centre allows a station to be selected and will display
								- More detailed occupancy information

								- The prediction of the number of bikes in three hours based on previous trends and the mm of rain fall predicted

								- A histogram which displays the average daily information of available bikes/available stands for that station

								- Daily average mm of rain. 

* The second select option displays hourly average station information on the available stands/available bikes for that station and the hourly average mm of rain. 


====================
extra functionality
====================

* 	We used the Google maps geolocation service to display a unique (bouncy) marker which centres on the user’s location. Unfortunately, we had to later remove this feature since it was not supported 	on the EC2 and when we tried to implement it via the server, it broke our map. (Fig 7.)

* 	Each station marker has been customised to display with a different colour based on occupancy; green markers mean the station has at least 60% of its bikes available, orange means the station is 	at 20-60% bike capacity, and red means that there are less than 20% of the bikes left.

* 	In addition, each marker bounces twice on the map when selected from the dropdown menu, so users can see where a station is located if they only know its name

* 	Each marker has a left click option that displays station data for its location

* 	Each marker answers to a double click call which shows walking directions from the user’s location

* 	A hamburger menu displays on the left-hand side of the page when clicked, containing social media links to all things Dublin Bikes

* 	Customised weather icons display in the page header along with current time and temperature and a 3h weather prediction

* 	To improve the user experience the page displays a loader gif of a moving bike while the backend functions are taking place


====
Note
====

Project Created By; Mary Catherine Tyrrell, Ciara Dillon, Mariyana Levova. 

This project has been set up using PyScaffold 3.0.1. For details and usage
information on PyScaffold see http://pyscaffold.org/.
