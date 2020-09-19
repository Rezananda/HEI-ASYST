function slideShow(){
  jQuery('#slideup').slideDown(600);
  document.getElementById("backdrop").style.width = "100%";
  document.getElementById("backdrop").style.opacity = "0.5";    
}

function slideHide(){
  jQuery('#slideup').slideUp(600);
  document.getElementById("backdrop").style.width = "0";
  document.getElementById("backdrop").style.opacity = "0";
}

function slideShowAdd(){
  jQuery('#slideup').slideUp(600);
  jQuery('#slideupadd').slideDown(600);
  document.getElementById("backdrop").style.width = "100%";
  document.getElementById("backdrop").style.opacity = "0.5";    
}

function slideHideAdd(){
  jQuery('#slideupadd').slideUp(600);
  document.getElementById("backdrop").style.width = "0";
  document.getElementById("backdrop").style.opacity = "0";
}

function handleSelect() {
  // console.log(document.getElementById("conditions").value)
  // console.log(document.getElementById("work_statuss").value)
  if (document.getElementById("attend").value == "Tidak Hadir") {
      document.getElementById("reasonAttend").style.display = "block";
      document.getElementById('work_statuss').value = "-";
  } else {
      document.getElementById("reasonAttend").style.display = "none";
      document.getElementById('otherAttend').value = "-";
  }

  if (document.getElementById("reasonAttends").value == "Lainnya") {
      document.getElementById("otherAttend").style.display = "block";
  } else {
      document.getElementById("otherAttend").style.display = "none";
  }
}

function handleSelectSick() {

  if (document.getElementById("condition").value == "Sakit") {
      document.getElementById("sickChoice").style.display = "block";
  } else {
      document.getElementById("sickChoice").style.display = "none";
      document.getElementById('sick').value = "-";
  }

  if (document.getElementById("sickChoices").value == "Lainnya") {
      document.getElementById("otherSick").style.display = "block";
  } else {
      document.getElementById("otherSick").style.display = "none";
  }
}


function handleSelectWFO() {
  
  if (document.getElementById("work_status").value == "WFO") {
      document.getElementById("wfoStatus").style.display = "block";
  } else {
      document.getElementById("wfoStatus").style.display = "none";
      document.getElementById('work_description').value = "-";
  }
}

