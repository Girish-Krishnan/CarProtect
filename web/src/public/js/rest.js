var vibration_1 = document.getElementById("vib_1")
var vibration_2 = document.getElementById("vib_2")
var pir_1 = document.getElementById("people_1")
var pir_2 = document.getElementById("people_2")

var latitude = document.getElementById("lat")
var longitude = document.getElementById("long")
var gpsdisplay = document.getElementById("gpsdisplay")
var stream  = setInterval(function() {}, 1000);

var username_box = document.getElementById("username");
var password_box = document.getElementById("password");

var image_live = document.getElementById("live_stream");

var map_lat = 32.8755662;
var map_long = -117.2323252;

function initMap() {
    // The location of Uluru
    const uluru = { lat: map_lat, lng: map_long };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("gpsdisplay"), {
      zoom: 4,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }

function log_in() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    fetch('/unlock/' + username + '/' + password + '/')
        .then(response => response.json())
        .then(function(response) {
            if (response['username'] != "" && response['password'] != "") {
                username_box.value = "";
                password_box.value = "";
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
                console.log(response);
                if(response['pir'] == 1) {
                    pir_1.src = "person_1.png".split("?")[0] + "?" + new Date().getTime();
                    pir_2.src = "warning.png".split("?")[0] + "?" + new Date().getTime();
                    //console.log("PIR 1");
                }
                else {
                    pir_1.src = "person_0.png".split("?")[0] + "?" + new Date().getTime();
                    pir_2.src = "good.png".split("?")[0] + "?" + new Date().getTime();
                }

                if(response['vibration'] >= 2) {
                    vibration_1.src = "vib_1.gif".split("?")[0] + "?" + new Date().getTime();
                    vibration_2.src = "warning.png".split("?")[0] + "?" + new Date().getTime();
                }

                else {
                    vibration_1.src = "vib_0.gif".split("?")[0] + "?" + new Date().getTime();
                    vibration_2.src = "good.png".split("?")[0] + "?" + new Date().getTime();
                }

              //  vibration.innerHTML = "Vibrations: " + response['vib'];
               // acc.innerHTML = "Accelerations: " + response['ax'] + ", " + response['ay'] + ", " + response['az'];
            
                // latitude.innerHTML = "Latitude: " + response['lat'];
                // longitude.innerHTML = "Longitude: " + response['long'];
                
                //gpsdisplay.innerHTML = "<iframe src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3834.307389525948!2d" + response['long'] + "!3d" + response['lat'] + "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x32b4f401e6728a1e!2zMTbCsDAyJzU4LjMiTiAxMTHCsDIyJzM3LjQiVw!5e0!3m2!1sen!2sus!4v1652921872656!5m2!1sen!2sus\" width=\"300\" height=\"500\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>";

                // var map;
                // var geocoder;
                // var mapOptions = { center: new google.maps.LatLng(0.0, 0.0), zoom: 2,
                //                 mapTypeId: google.maps.MapTypeId.ROADMAP };

                // function initialize() {
                // var myOptions = {
                //     center: new google.maps.LatLng(40.713955826286046, -73.992919921875 ),
                //     zoom: 15,
                //     mapTypeId: google.maps.MapTypeId.ROADMAP
                // };

                // var map = new google.maps.Map(document.getElementById("gpsdisplay"), myOptions);

                // }
                // //This will render map on load
                // window.addEventListener('load', initialize);

                
                
                image_live.src = image_live.src.split("?")[0] + "?" + new Date().getTime();
                image_live.innerHTML = "";

                // Initialize and add the map
  
  window.initMap = initMap;
  map_lat = response['lat'];
    map_long = response['long'];
  
            })

    },500);
}