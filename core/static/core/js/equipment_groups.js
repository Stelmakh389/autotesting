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

    const csrfToken = getCookie('csrftoken');

    // Обработка выбора количества элементов на странице
    const perPageSelect = document.getElementById('per-page-select');
    if (perPageSelect) {
        perPageSelect.addEventListener('change', function() {
            const searchParams = new URLSearchParams(window.location.search);
            searchParams.set('per_page', this.value);
            window.location.search = searchParams.toString();
        });
    }

    // Обработка массового выбора
    const selectAllCheckbox = document.getElementById('select-all');
    const groupCheckboxes = document.querySelectorAll('.group-checkbox');
    const bulkDeleteButton = document.getElementById('bulk-delete-groups');

    function updateBulkDeleteButton() {
        const checkedBoxes = document.querySelectorAll('.group-checkbox:checked');
        if (bulkDeleteButton) {
            bulkDeleteButton.disabled = checkedBoxes.length === 0;
        }
    }

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            groupCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkDeleteButton();
        });
    }

    groupCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(groupCheckboxes).every(cb => cb.checked);
            const someChecked = Array.from(groupCheckboxes).some(cb => cb.checked);
            
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = allChecked;
                selectAllCheckbox.indeterminate = someChecked && !allChecked;
            }
            
            updateBulkDeleteButton();
        });
    });

    // Массовое удаление групп
    if (bulkDeleteButton) {
        bulkDeleteButton.addEventListener('click', function() {
            const checkedBoxes = document.querySelectorAll('.group-checkbox:checked');
            const selectedIds = Array.from(checkedBoxes).map(cb => cb.value);

            if (selectedIds.length === 0) {
                alert('Выберите группы для удаления');
                return;
            }

            if (confirm('Вы уверены, что хотите удалить выбранные группы?')) {
                fetch('/equipment/groups/bulk-delete/', {
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
                    alert('Произошла ошибка при удалении групп');
                });
            }
        });
    }

    // Копирование группы
    document.querySelectorAll('.copy-group').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const groupId = this.dataset.id;

            fetch(`/equipment/groups/${groupId}/copy/`, {
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
                alert('Произошла ошибка при копировании группы');
            });
        });
    });
});