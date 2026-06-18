// Google Sheet connect code
(function () {
  const scriptURL = "https://script.google.com/macros/s/AKfycbyKGziey4KlEAoceB4HkygpkQjaRgd_xDMBCP8WU2xBq_ZXZoVk21E4a9nMBMtmmP8w0Q/exec";

  // Handle contact section form
  const form1 = document.forms['google-sheet1'];
  if (form1) {
    form1.addEventListener('submit', e => {
      e.preventDefault();
      fetch(scriptURL, { method: 'POST', body: new FormData(form1) })
        .then(response => alert("Thanks for Contacting us..! We Will Contact You Soon..."))
        .catch(error => console.error('Error!', error.message));
    });
  }

  // Handle modal contact form
  const form2 = document.forms['google-sheet2'];
  if (form2) {
    form2.addEventListener('submit', e => {
      e.preventDefault();
      fetch(scriptURL, { method: 'POST', body: new FormData(form2) })
        .then(response => alert("Thanks for Contacting us..! We Will Contact You Soon..."))
        .catch(error => console.error('Error!', error.message));
    });
  }
})();
