document.addEventListener('DOMContentLoaded', function() {
    // Функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Инициализация переменных
    const selectAllCheckbox = document.getElementById('select-all');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const bulkDeleteButton = document.getElementById('bulk-delete');
    const csrfToken = getCookie('csrftoken');

    // Функция обновления состояния кнопки удаления
    function updateBulkDeleteButton() {
        const checkedBoxes = document.querySelectorAll('.item-checkbox:checked');
        if (bulkDeleteButton) {
            bulkDeleteButton.disabled = checkedBoxes.length === 0;
        }
    }

    // Обработчик для выбора всех элементов
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkDeleteButton();
        });
    }

    // Обработчики для отдельных чекбоксов
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(itemCheckboxes).every(cb => cb.checked);
            const someChecked = Array.from(itemCheckboxes).some(cb => cb.checked);
            
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = allChecked;
                selectAllCheckbox.indeterminate = someChecked && !allChecked;
            }
            
            updateBulkDeleteButton();
        });
    });

    // Обработчик массового удаления
    if (bulkDeleteButton) {
        bulkDeleteButton.addEventListener('click', function() {
            const checkedBoxes = document.querySelectorAll('.item-checkbox:checked');
            const selectedIds = Array.from(checkedBoxes).map(cb => cb.value);

            if (selectedIds.length === 0) {
                alert('Выберите элементы для удаления');
                return;
            }

            if (confirm('Вы уверены, что хотите удалить выбранные элементы?')) {
                fetch('/equipment/bulk-delete/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        ids: selectedIds
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        window.location.reload();
                    } else {
                        throw new Error(data.message || 'Ошибка при удалении');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Произошла ошибка при удалении элементов');
                });
            }
        });
    }

    // Обработчик копирования оборудования
    document.querySelectorAll('.copy-equipment').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const equipmentId = this.dataset.id;

            fetch(`/equipment/${equipmentId}/copy/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    window.location.reload();
                } else {
                    throw new Error(data.message || 'Ошибка при копировании');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при копировании оборудования');
            });
        });
    });
});