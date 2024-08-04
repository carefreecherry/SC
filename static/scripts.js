document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const previewImage = document.getElementById('previewImage');
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        document.getElementById('uploadText').style.display = 'none';
    }

    if (file) {
        reader.readAsDataURL(file);
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.sheet_count !== undefined) {
            document.getElementById('sheetCount').textContent = `Number of Sheets: ${data.sheet_count}`;
            document.getElementById('processedImage').src = data.processed_image_path;
            document.getElementById('processedImage').style.display = 'block';
        } else {
            document.getElementById('sheetCount').textContent = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
