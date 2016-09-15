function doClick() {
      var el = document.getElementsByName("image")[0]
      if (el) {
        el.click();
      }
    }
    function handleFiles(files) {
	 var file = files[0];
      var d = document.getElementById("fileList");
      if (!files.length) {
        d.innerHTML = "No selecciono ninguna foto";
      } else {
          while (d.hasChildNodes()) {
              d.removeChild(d.lastChild);
           }
          var img = document.createElement("img");
	     img.name = "image"
          img.src = window.URL.createObjectURL(file);
          img.width = 200;
	     img.height = 200;
          img.onload = function() {
            window.URL.revokeObjectURL(this.src);
          }
          d.appendChild(img);
          
          var info = document.createElement("div");
          info.innerHTML = file.name + ": " + file.size + " bytes";
          d.appendChild(info);
      }
    }
