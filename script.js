document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var photo = document.getElementById('photo').files[0];

    var reader = new FileReader();

    reader.readAsDataURL(photo);
    reader.onload = function(event) {
        localStorage.setItem('photoData', event.target.result);
    };

    var formData = new FormData();
    formData.append('firstName', firstName);
    formData.append('lastName', lastName);
    formData.append('photo', photo);

    fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('result', data.result);
        localStorage.setItem('firstName', data.firstName);
        localStorage.setItem('lastName', data.lastName);
        
        window.location.href = 'result.html';
    })
    .catch(error => console.error('Error:', error));
});
