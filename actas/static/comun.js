const fileInput = document.querySelector('#documento input[type=file]');
  fileInput.onchange = function() {
    if (fileInput.files.length > 0) {
      const fileName = document.querySelector('#documento .file-name');
      fileName.textContent = fileInput.files[0].name;
    }
  }

//MESSAGES (sólo uno)
article = document.querySelector(".message");
btnMessage = document.querySelector(".message .delete");
if (btnMessage) {
        btnMessage.addEventListener('click', function() {
                article.parentNode.removeChild(article);
        });
}


const fileName = document.querySelector('#documento .file-name');
btnDoc = document.querySelector("#delete_doc");
if (btnDoc) {
        btnDoc.addEventListener('click', function() {
                fileName.textContent = "Sin archivo";
        });
}
