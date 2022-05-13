var vibration = document.getElementById("vib")
var pir = document.getElementById("pir")
var acc = document.getElementById("acc")
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
                    pir.innerHTML = "Motion of a Person Nearby: Yes";
                }
                else {
                    pir.innerHTML = "Motion of a Person Nearby: No";
                }

                vibration.innerHTML = "Vibrations: " + response['vib'];
            
                acc.innerHTML = "Accelerations: " + response['ax'] + ", " + response['ay'] + ", " + response['az'];
                if(response['lat'] != "0.000000") {
                latitude.innerHTML = "Latitude: " + response['lat'];
                longitude.innerHTML = "Longitude: " + response['long'];
                }
                gpsdisplay.innerHTML = " <script type=\"text/javascript\" src=\"http://maps.google.com/maps/api/js?sensor=false\"></script><div id=\"map\" style=\"width: 400px; height: 300px\"></div><script type=\"text/javascript\"> var myOptions = {zoom: 8,center: new google.maps.LatLng(" + response['lat'] + "," + response['long'] + "),mapTypeId: google.maps.MapTypeId.ROADMAP};var map = new google.maps.Map(document.getElementById(\"map\"), myOptions);</script>"

            })

    },2000);
}