//Google Sheet connect code
var scriptURL = "https://script.google.com/macros/s/AKfycbyKGziey4KlEAoceB4HkygpkQjaRgd_xDMBCP8WU2xBq_ZXZoVk21E4a9nMBMtmmP8w0Q/exec";
var form = document.forms['google-sheet1'];
form.addEventListener('submit', e => {
e.preventDefault()
fetch(scriptURL, { method: 'POST', body: new FormData(form)})
  .then(response => alert("Thanks for Contacting us..! We Will Contact You Soon..."))
  .catch(error => console.error('Error!', error.message))
});