console.log("loaded");

var showPassword = document.querySelector("#show-password");
var password = document.querySelector("#password");
var para = document.querySelector("#para");
password.addEventListener("keyup", pass);
function pass(e) {
  var passValue = e.target.value;
  if (passValue.length < 6 && passValue.length > 0) {
    para.innerHTML = "Password must be 6 characters long";
    para.style.color = "#d9534f";
    para.style.fontWeight = "bold";
    para.style.padding = "10px";
    para.style.backgroundColor = "#f9d6d5";
    para.style.border = "1px solid #d9534f";
    para.style.borderRadius = "5px";
  } else {
    para.innerHTML = "";
    para.style.color = "";
    para.style.fontWeight = "";
    para.style.padding = "";
    para.style.backgroundColor = "";
    para.style.border = "";
    para.style.borderRadius = "";
  }
}
function showPass() {
  if (showPassword.checked) {
    password.type = "text";
  } else {
    password.type = "password";
  }
}
