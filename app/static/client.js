var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
  el("result-label").innerHTML = ``;
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to segment!");
	
  el("result-label").innerHTML = ``;
  el("analyze-button").innerHTML = "Segmenting Items...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
	  
	  document.getElementById('image-picked').src="/static/result.png?" + new Date().getTime();
	  
      var response = JSON.parse(e.target.responseText);
      el("result-label").innerHTML = `${response["status"]}`;
    }
    el("analyze-button").innerHTML = "Apply Segmentation";
  };

  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

