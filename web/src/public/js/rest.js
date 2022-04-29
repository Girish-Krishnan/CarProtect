var vibration = document.getElementById("vib")
var pir = document.getElementById("pir")
var acc = document.getElementById("acc")
var latitude = document.getElementById("lat")
var longitude = document.getElementById("long")
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
                
                if(response['vib'] == "1") {
                    vibration.innerHTML = "Vibrations: Yes";
                }
                else {
                    vibration.innerHTML = "Vibrations: No";
                }

                acc.innerHTML = "Accelerations: " + response['ax'] + ", " + response['ay'] + ", " + response['az'];
                latitude.innerHTML = "Latitude: " + response['lat'];
                longitude.innerHTML = "Longitude: " + response['long'];


            })

    },2000);
}