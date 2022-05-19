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

                if(response['vibration'] == "4" | response['vibration'] == "5" | response['vibration'] == "6") {
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
                
                gpsdisplay.innerHTML = "<iframe src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3834.307389525948!2d" + response['long'] + "!3d" + response['lat'] + "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x32b4f401e6728a1e!2zMTbCsDAyJzU4LjMiTiAxMTHCsDIyJzM3LjQiVw!5e0!3m2!1sen!2sus!4v1652921872656!5m2!1sen!2sus\" width=\"300\" height=\"500\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>";
            })

    },2000);
}