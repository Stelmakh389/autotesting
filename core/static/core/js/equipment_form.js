function openEquipmentForm(pk = null) {
    const url = pk ? 
        `/equipment/${pk}/update/` : 
        '/equipment/create/';
        
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.form) {
                const modal = new bootstrap.Modal(document.getElementById('equipmentFormModal'));
                document.getElementById('equipmentForm').innerHTML = data.form;
                modal.show();
            }
        });
}

function submitEquipmentForm() {
    const form = document.getElementById('equipmentForm');
    const formData = new FormData(form);
    const errorDiv = document.getElementById('formErrors');
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('equipmentFormModal'));
            modal.hide();
            window.location.reload();
        } else {
            errorDiv.style.display = 'block';
            errorDiv.innerHTML = '<h5>Пожалуйста, исправьте следующие ошибки:</h5>';
            Object.keys(data.errors).forEach(key => {
                errorDiv.innerHTML += `<p>${key}: ${data.errors[key].join(', ')}</p>`;
            });
        }
    });
}