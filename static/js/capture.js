(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

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
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    canvasCircleOverlay = document.getElementById('canvas-circle-overlay');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
    canvas.setAttribute('width', 100);
    canvas.setAttribute('height', 100);

    navigator.getMedia = ( navigator.getUserMedia ||
                           navigator.webkitGetUserMedia ||
                           navigator.mozGetUserMedia ||
                           navigator.msGetUserMedia);

    navigator.getMedia(
      {
        video: true,
        audio: false
      },
      function(stream) {
        if (navigator.mozGetUserMedia) {
          video.mozSrcObject = stream;
        } else {
          var vendorURL = window.URL || window.webkitURL;
          video.src = vendorURL.createObjectURL(stream);
        }
        video.play();
      },
      function(err) {
        console.log("An error occured! " + err);
      }
    );

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
        
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        canvasCircleOverlay.setAttribute('width', width);
        canvasCircleOverlay.setAttribute('height', height);

        // Draw the circle overlay
        var context = canvasCircleOverlay.getContext('2d');
        context.beginPath();
        context.lineWidth = 20;
        context.strokeStyle = "#f1d3ff";
        context.globalAlpha = 0.5;
        context.arc(width/2, height/2, 90, 0, Math.PI * 2, true); // Outer circle
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
    var ref = storageRef.child("/images/" + id + ".png");
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
        xhr.open('GET', baseUrl + "/images/" + id, true);
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

  // Set up our event listener to run the startup process
  // once loading is complete.
  window.addEventListener('load', startup, false);
})();
