var vibration_1 = document.getElementById("vib_1")
var vibration_2 = document.getElementById("vib_2")
var pir_1 = document.getElementById("people_1")
var pir_2 = document.getElementById("people_2")

var latitude = document.getElementById("lat")
var longitude = document.getElementById("long")
var gpsdisplay = document.getElementById("gpsdisplay")
var stream  = setInterval(function() {}, 1000);

function log_in() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    fetch('/unlock/' + username + '/' + password + '/')
        .then(response => response.json())
        .then(function(response) {
            if (response['username'] != "" && response['password'] != "") {
                clearInterval(stream);
                stream_data(response['username'], response['password']);
            }
            else {
                alert("Invalid username or password");
            }
            })
        }

function stream_data(username,password) {
    stream = setInterval(function() {
    
        fetch('/stream_data/' + username + '/' + password + '/')
            .then(response => response.json())
            .then(function(response) {
                if(response['pir'] == "1") {
                    pir_1.innerHTML = "<img src=\'person_1.png\'>";
                    pir_2.innerHTML = "<img src=\'warning.png\'>";
                }
                else {
                    pir_1.innerHTML = "<img src=\'person_0.png\'>";
                    pir_2.innerHTML = "<img src=\'good.png\'>";
                }

                if(response['vibration'] > "4") {
                    vibration_1.innerHTML = "<img src=\'vib_1.gif\'>";
                    vibration_2.innerHTML = "<img src=\'warning.png\'>";
                }

                else {
                    vibration_1.innerHTML = "<img src=\'vib_0.gif\'>";
                    vibration_2.innerHTML = "<img src=\'good.png\'>";
                }

              //  vibration.innerHTML = "Vibrations: " + response['vib'];
               // acc.innerHTML = "Accelerations: " + response['ax'] + ", " + response['ay'] + ", " + response['az'];
            
                // latitude.innerHTML = "Latitude: " + response['lat'];
                // longitude.innerHTML = "Longitude: " + response['long'];
                
                gpsdisplay.innerHTML = " <script type=\"text/javascript\" src=\"http://maps.google.com/maps/api/js?sensor=false\"></script><div id=\"map\" style=\"width: 400px; height: 300px\"></div><script type=\"text/javascript\"> var myOptions = {zoom: 8,center: new google.maps.LatLng(" + response['lat'] + "," + response['long'] + "),mapTypeId: google.maps.MapTypeId.ROADMAP};var map = new google.maps.Map(document.getElementById(\"map\"), myOptions);</script>"

            })

    },2000);
}