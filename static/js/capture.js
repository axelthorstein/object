(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  // TODO: This is hardcoded to fit the Pixel 2 XL aspect ratio of 18:9
  // for testing on desktop Chrome, but in production lines 25 & 26 should be uncommented.
  var width = 360;    // We will scale the photo width to this
  var height = 720;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  function startup() {
    // height = screen.height;
    // width = screen.width;
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    canvasCircleOverlay = document.getElementById('canvas-circle-overlay');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    navigator.getMedia = ( navigator.getUserMedia ||
                           navigator.webkitGetUserMedia ||
                           navigator.mozGetUserMedia ||
                           navigator.msGetUserMedia);

    navigator.getMedia(
      {
        audio: false,
        // asks the users camera for a a specfic aspect ratio, but if it isn't
        // able to oblige it give up to the min/max values specfied
        video: {
          width: { min: 360, ideal: width, max: 1440 },
          height: { min: 720, ideal: height, max: 2880 },
          // prefer that the rear camera is used. If on mobile this will be true,
          // if on desktop the front camera will be used. In production this should
          // be disabled
          facingMode: "environment",
          // limit the video framerate for streaming so that 
          frameRate: { ideal: 30, max: 60 }
        }
      },
      function(stream) {
        if (navigator.mozGetUserMedia) {
          video.mozSrcObject = stream;
        } else {
          try {
            video.srcObject = stream;
          } catch (error) {
            video.src = window.URL.createObjectURL(mediaSource);
          }
        }
        video.play();
      },
      function(err) {
        console.log(err.name + ": " + err.message); // always check for errors at the end.
      }
    );

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        canvasCircleOverlay.setAttribute('width', width * 2);
        canvasCircleOverlay.setAttribute('height', height * 2);

        // Draw the circle overlay
        var context = canvasCircleOverlay.getContext('2d');
        context.beginPath();
        context.lineWidth = 45;
        context.strokeStyle = "#f1d3ff";
        context.globalAlpha = 0.75;
        var overlaySize = 200
        context.arc(width, height, overlaySize, 0, Math.PI * 2, true); // Outer circle
        context.stroke();

        streaming = true;
      }
    }, false);


    startbutton.addEventListener('click', function(ev){

      takepicture();
      ev.preventDefault();
    }, false);
    
    clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {



    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    if (photo != null) {
      photo.setAttribute('src', data);
    }
  }
  
  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

  function takepicture() {
    var storageRef = firebase.storage().ref();
    var id = (Math.floor(Math.random() * (1000000 - 1)) + 1).toString();
    var ref = storageRef.child("/products/" + id + ".png");
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
    
      var data = canvas.toDataURL('image/png');
        ref.putString(data, 'data_url').then(function(snapshot) {
          console.log('Uploaded a data_url string!');
          var xhr = new XMLHttpRequest();
          var baseUrl = window.location.href.split('/capture')[0];
          xhr.open('GET', baseUrl + "/products/" + id, true);
          xhr.send();
          xhr.onreadystatechange = processRequest;
          function processRequest(e) {
              if (xhr.readyState == 4 && xhr.status == 200) {
                  console.log(xhr.responseText);
                  window.location.replace(xhr.responseText);
              }
          }
        });
      if (photo != null) {
        photo.setAttribute('src', data);
      }
    } else {
      clearphoto();
    }
  }

  // To run a function every second with backoff. 
  // https://codereview.stackexchange.com/questions/125555/javascript-to-fire-event-every-second-until-10s-then-gradually-increase?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
  // heartbeat(10000, 1000, 10000000, function(now, interval){
  //     console.log('beat', interval / 1000);
  // });

  function heartbeat(delay, interval, duration, callback){
    var now = Date.now();
    var end = now + delay + duration;
    var inc = function(v){ return v; };
    function beat(){
      var now = Date.now();
      if(now < end){
        callback(now, interval);
        interval = inc(interval);
        timeout = setTimeout(beat, interval);
      }
    }
    var timeout = setTimeout(beat, interval);
    var delayTimeout = setTimeout(function(){
      inc = function(v){ return Math.pow(v, 1.15); }
    }, delay);
    return function(){
      clearTimeout(timeout);
      clearTimeout(delayTimeout);
    }
  }

  // Set up our event listener to run the startup process
  // once loading is complete.
  window.addEventListener('load', startup, false);
})();
