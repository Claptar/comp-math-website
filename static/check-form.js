document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('button').disabled = true;
});

let dictCorrect = {'mass1': false, 'mass2': false, 'thread1': false, 'thread2': false};

function enforceMinMax(el) {
  if(el.value != ""){
    if(parseInt(el.value) < parseInt(el.min) || parseInt(el.value) > parseInt(el.max)){

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
  console.log(dictCorrect)
  inputCorrect = true;
  for (let key of Object.keys(dictCorrect)) {
    inputCorrect = inputCorrect & dictCorrect[key];
  }

  if (inputCorrect == true) {
    document.getElementById('button').disabled = false;
  }
}
