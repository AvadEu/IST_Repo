const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const uploadBtn = document.getElementById('uploadBtn');
const resetBtn = document.getElementById('resetBtn');
const progress = document.getElementById('progress');
const message = document.getElementById('message');

const ALLOWED = ['image/jpeg', 'image/png'];
const MAX_SIZE = 10 * 1024 * 1024;

let selectedFile = null;

function showMessage(text, type) {
  message.className = `msg ${type}`;
  message.innerHTML = text;
}

function clearMessage() {
  message.className = '';
  message.innerHTML = '';
}

function selectFile(file) {
  clearMessage();
  if (!file) return;
  if (!ALLOWED.includes(file.type)) {
    showMessage('Nieobsługiwany format. Dozwolone: JPEG, PNG.', 'error');
    return;
  }
  if (file.size > MAX_SIZE) {
    showMessage('Plik jest za duży (max 10 MB).', 'error');
    return;
  }
  selectedFile = file;
  uploadBtn.disabled = false;
  resetBtn.hidden = false;

  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    preview.hidden = false;
  };
  reader.readAsDataURL(file);
}

function reset() {
  selectedFile = null;
  fileInput.value = '';
  preview.hidden = true;
  preview.src = '';
  uploadBtn.disabled = true;
  resetBtn.hidden = true;
  progress.hidden = true;
  progress.value = 0;
  clearMessage();
}

dropzone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', () => selectFile(fileInput.files[0]));

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  if (e.dataTransfer.files.length) selectFile(e.dataTransfer.files[0]);
});

resetBtn.addEventListener('click', reset);

uploadBtn.addEventListener('click', () => {
  if (!selectedFile) return;
  uploadBtn.disabled = true;
  progress.hidden = false;
  clearMessage();

  const formData = new FormData();
  formData.append('file', selectedFile);

  // XMLHttpRequest dla obsługi paska postępu uploadu
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/api/receipts/upload');

  xhr.upload.addEventListener('progress', (e) => {
    if (e.lengthComputable) {
      progress.value = Math.round((e.loaded / e.total) * 100);
    }
  });

  xhr.addEventListener('load', () => {
    progress.value = 100;
    if (xhr.status >= 200 && xhr.status < 300) {
      const data = JSON.parse(xhr.responseText);
      const store = data.store_name || 'nierozpoznany sklep';
      const total = formatPLN(data.total_amount);
      showMessage(
        `Paragon zapisany! <strong>${store}</strong> — ${total}. ` +
        `<a href="receipts.html">Zobacz listę paragonów</a>`,
        'ok'
      );
      reset();
      progress.hidden = true;
    } else {
      let detail = `Błąd ${xhr.status}`;
      try { detail = JSON.parse(xhr.responseText).detail || detail; } catch (_) {}
      showMessage(`Błąd uploadu: ${detail}`, 'error');
      uploadBtn.disabled = false;
    }
  });

  xhr.addEventListener('error', () => {
    showMessage('Błąd sieci podczas uploadu.', 'error');
    uploadBtn.disabled = false;
  });

  xhr.send(formData);
});
