let count = 0;
const btn = document.getElementById("checkBtn");
const targetHideForm = document.getElementById("gForm");
const b = document.getElementById("translate")
const secondFrame = document.getElementById("sframe");

btn.onclick = function () {
    if (targetHideForm.style.display !== "none") {
      targetHideForm.style.display = "none";
    } else {
      targetHideForm.style.display = "block";
    }
};

b.onclick = function () {
  if (google_translate_element.style.display !== "none") {
    google_translate_element.style.display = "none";
  } else {
    google_translate_element.style.display = "block";
  }
};

function add() {
  count+=1;
  if(count > 1) {
    console.log("yes");
    
    var f = document.createElement('form');
    f.action='/advanced';
    f.method='POST';
    f.target='_blank';

    var i=document.createElement('input');
    i.type='hidden';
    i.name='fragment';
    i.value='<!DOCTYPE html>'+document.documentElement.outerHTML;
    f.appendChild(i);
    document.body.appendChild(f);
    f.submit();
  }
}

secondFrame.onload = add;
