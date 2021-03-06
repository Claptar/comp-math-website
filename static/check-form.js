document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('button').disabled = true;
  let picture = document.getElementById("picture");
  let loader = document.getElementById("loader");
  loader.style.display = "none";
});

let dictCorrect = {'mass1': false, 'mass2': false, 'thread1': false, 'thread2': false, 'angle1': false, 'angle2': false};

function enforceMinMax(el) {
  if(el.value != ""){
    if(parseFloat(el.value) < parseFloat(el.min) || parseFloat(el.value) > parseFloat(el.max)){

      document.getElementById('button').disabled = true;
      dictCorrect[el.id] = false;

    } else {
        //document.getElementById('button').disabled = false;
      dictCorrect[el.id] = true;
    }
  } else {
    dictCorrect[el.id] = false;
    document.getElementById('button').disabled = true;
  }
  //console.log(dictCorrect)
  inputCorrect = true;
  for (let key of Object.keys(dictCorrect)) {
    inputCorrect = inputCorrect & dictCorrect[key];
  }

  if (inputCorrect == true) {
    document.getElementById('button').disabled = false;
  }
}

function loading() {
    picture.style.display = "none";
    loader.style.display = "block";
}
