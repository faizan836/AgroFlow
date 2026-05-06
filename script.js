let video = document.getElementById("video")

// Open Camera
function openCamera(){

navigator.mediaDevices.getUserMedia({video:true})
.then(function(stream){

video.srcObject = stream

})
.catch(function(error){

console.log("Camera error:", error)

})

}


// Capture Photo + GPS + Send to Backend
function capturePhoto(){

let canvas = document.getElementById("canvas")
let context = canvas.getContext("2d")

context.drawImage(video,0,0,300,200)

let imageData = canvas.toDataURL("image/png")

document.getElementById("resultText").innerText =
"Analyzing farm image with AI..."

navigator.geolocation.getCurrentPosition(function(position){

let lat = position.coords.latitude
let lon = position.coords.longitude

fetch("http://127.0.0.1:5000/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
image:imageData,
lat:lat,
lon:lon
})

})

.then(res=>res.json())

.then(data=>{

fetch("https://nominatim.openstreetmap.org/reverse?format=json&lat="+data.lat+"&lon="+data.lon)

.then(res=>res.json())

.then(place=>{

let locationName =
place.address.city ||
place.address.town ||
place.address.village ||
place.address.state

document.getElementById("resultText").innerText =
"Soil: " + data.soil +
" | Best Crop: " + data.crop +
" | Location: " + locationName

})

})

.catch(error=>{

console.log("Prediction error:", error)

})

})

}


// Weather Check
function checkWeather(){

let city = document.getElementById("city").value

fetch("http://127.0.0.1:5000/weather",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
city:city
})

})

.then(res=>res.json())

.then(data=>{

document.getElementById("weatherResult").innerText =
"Temp: "+data.temperature+
"°C | Humidity: "+data.humidity+
"% | Weather: "+data.weather+
" | Advice: "+data.advice

})

.catch(error=>{

console.log("Weather error:", error)

})

}


// 📍 Location Based Crop Suggestion
function getLocation(){

navigator.geolocation.getCurrentPosition(function(position){

let lat = position.coords.latitude
let lon = position.coords.longitude

fetch("http://127.0.0.1:5000/location_crop",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({

lat:lat,
lon:lon

})

})

.then(res=>res.json())

.then(data=>{

document.getElementById("resultText").innerText =
"Recommended Crop: " + data.crop

})

.catch(error=>{

console.log("Location error:", error)

})

})

}