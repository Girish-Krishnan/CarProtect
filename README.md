*Team Members*

Girish Krishnan, Anish Sharma, Ian Tanuwidjaja, and Hamza Khan
___

# ECE 140B: CarProtect

Hello! This repository contains all the code files for our project. The complete demo video can be found at: https://youtu.be/MSkuZj5Wf60 

___

## How the Code is Organized + Instructions to Run the Code

The __ESP 32__ folder contains the Arduino code that needs to be uploaded to the board. The *CameraWebServerGirish* code is not used in this project per se, but is a useful tutorial on using the ESP32 cam, that inspired us to build the rest of the project.

Inside the __ESP 32__ folder, you can find the __CamUpload__ folder, which contains the code that needs to be uploaded to the ESP32 Cam. The __CarProtect_ESP32__ folder contains the code that needs to be uploaded to the ESP32 Wrover Module board.

Once the code is uploaded to each board, remove all connections to the ESP32 cam. Then, connect the 5V pin of the ESP32 cam to the 5V-OUT pin of the ESP32 Wrover Module, and connect the ground pin of the ESP32 cam to the ground pin of the Wrover module. Then, connect the ESP32 Wrover module to a power source.

The __web__ folder contains the code necessary for the web server and database used for our full-stack IoT project. This involves the basic server architecture we learned in ECE 140A, and we have a Docker container with the web server + MySQL database. This is hosted via DigitalOcean.

Link: http://164.92.89.132/