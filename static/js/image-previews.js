document.addEventListener('DOMContentLoaded', function () {
  const input   = document.getElementById('id_images');   // hidden <input type="file" multiple>
  const pickBtn = document.getElementById('btn-pick-images');
  const dz      = document.getElementById('image-dropzone');
  const previews= document.getElementById('image-previews');
  const summary = document.getElementById('selected-images');

  if (!input) return; // nothing to do

  // Prevent the browser from opening files on drop anywhere (outside editors)
  ['dragover', 'drop'].forEach(function (evtName) {
    window.addEventListener(evtName, function (e) {
      var isDropzone = false;
      if (e.target && typeof e.target.closest === 'function') {
        isDropzone = !!e.target.closest('#image-dropzone');
      }
      if (e.target === document.body || isDropzone) {
        e.preventDefault();
      }
    }, false);
  });

  // Config
  var MAX_FILES = 50;
  var MAX_MB    = 10;
  var ALLOWED   = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];

  // Track object URLs to revoke later
  var objectURLs = [];

  function bytesToMB(b){ return (b / (1024*1024)).toFixed(1); }

  function renderSummary(files) {
    if (!files.length) { if (summary) summary.textContent = ''; return; }
    if (summary) {
      var firstThree = Array.prototype.slice.call(files, 0, 3).map(function(f){ return f.name; }).join(', ');
      summary.textContent = files.length + ' selected (' + firstThree + (files.length > 3 ? '…' : '') + ')';
    }
  }

  function clearPreviews() {
    objectURLs.forEach(function(url){ URL.revokeObjectURL(url); });
    objectURLs = [];
    if (previews) previews.innerHTML = '';
  }

  function fileValid(f) {
    if (ALLOWED.indexOf(f.type) === -1) return { ok:false, msg: f.name + ': unsupported type' };
    if (f.size > MAX_MB * 1024 * 1024) return { ok:false, msg: f.name + ': over ' + MAX_MB + 'MB' };
    return { ok:true };
  }

  function addCards(files) {
    if (!previews) return;
    clearPreviews();
    Array.prototype.forEach.call(files, function (f) {
      var url = URL.createObjectURL(f);
      objectURLs.push(url);

      var col  = document.createElement('div'); col.className = 'col';
      var card = document.createElement('div'); card.className = 'preview-card';
      var img  = document.createElement('img'); img.alt = f.name; img.src = url;
      var meta = document.createElement('div'); meta.className = 'preview-meta';
      meta.textContent = f.name + ' — ' + bytesToMB(f.size) + ' MB';

      card.appendChild(img); card.appendChild(meta);
      col.appendChild(card);
      previews.appendChild(col);
    });
  }

  // Merge new files with existing input.files (allow adding in batches)
  function mergeIntoInput(newFiles) {
    var dt = new DataTransfer();
    Array.prototype.forEach.call(input.files || [], function (f) { dt.items.add(f); });
    newFiles.forEach(function (f) { dt.items.add(f); });

    while (dt.files.length > MAX_FILES) dt.items.remove(dt.files.length - 1);
    input.files = dt.files;
  }

  function handleFiles(selected) {
    var files = Array.prototype.slice.call(selected);
    var ok = [], errs = [];
    files.forEach(function (f) {
      var v = fileValid(f);
      if (v.ok) ok.push(f); else errs.push(v.msg);
    });
    if (errs.length) alert('Some files were skipped:\n\n' + errs.join('\n'));
    if (!ok.length) return;

    mergeIntoInput(ok);
    renderSummary(input.files);
    addCards(input.files);
  }

  // Button opens picker
  if (pickBtn) pickBtn.addEventListener('click', function(){ input.click(); });

  // Picker change
  input.addEventListener('change', function () {
    renderSummary(input.files);
    addCards(input.files);
  });

  // Drag & drop on the dropzone
  if (dz) {
    ['dragenter','dragover'].forEach(function (ev) {
      dz.addEventListener(ev, function (e) {
        e.preventDefault(); e.stopPropagation();
        dz.classList.add('dragover');
      });
    });
    ['dragleave','drop'].forEach(function (ev) {
      dz.addEventListener(ev, function (e) {
        e.preventDefault(); e.stopPropagation();
        dz.classList.remove('dragover');
      });
    });
    dz.addEventListener('drop', function (e) {
      var dropped = e.dataTransfer && e.dataTransfer.files;
      if (!dropped || !dropped.length) return;
      handleFiles(Array.prototype.slice.call(dropped));
    });
  }

  // Cleanup URLs on nav away
  window.addEventListener('beforeunload', clearPreviews);
});
