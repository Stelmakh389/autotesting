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
    const selectAllCheckbox = document.getElementById('selectAll');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const bulkActions = document.querySelector('.bulk-actions');
    const bulkDuplicateBtn = document.getElementById('bulkDuplicate');
    const csrfToken = getCookie('csrftoken');

    // Функция обновления видимости панели массовых действий
    function updateBulkActionsVisibility() {
        if (bulkActions) {
            const hasSelectedItems = [...itemCheckboxes].some(cb => cb.checked);
            bulkActions.style.display = hasSelectedItems ? 'flex' : 'none';
        }
    }

    // Обработчик для выбора всех элементов
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionsVisibility();
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
            
            updateBulkActionsVisibility();
        });
    });

    // Обработчик для одиночного копирования
    document.querySelectorAll('[data-action="duplicate"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const vehicleId = this.getAttribute('href').split('/').filter(Boolean).pop();

            fetch(`/vehicles/duplicate/${vehicleId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при копировании автомобиля');
            });
        });
    });

    // Обработчик для массового копирования
    if (bulkDuplicateBtn) {
        bulkDuplicateBtn.addEventListener('click', function() {
            const selectedIds = [...document.querySelectorAll('.item-checkbox:checked')]
                .map(cb => cb.value);
            
            if (selectedIds.length === 0) {
                alert('Пожалуйста, выберите элементы для копирования');
                return;
            }
            
            if (confirm(`Вы уверены, что хотите скопировать ${selectedIds.length} элементов?`)) {
                fetch('/vehicles/bulk-duplicate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ ids: selectedIds }),
                    credentials: 'same-origin'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        window.location.reload();
                    } else {
                        let errorMessage = data.message;
                        if (data.errors && data.errors.length > 0) {
                            errorMessage += '\n\n' + data.errors.join('\n');
                        }
                        alert(errorMessage);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Произошла ошибка при копировании');
                });
            }
        });
    }

    // Обработчик массового удаления
    document.querySelector('[data-action="bulk-delete"]')?.addEventListener('click', function() {
        const selectedIds = [...document.querySelectorAll('.item-checkbox:checked')]
            .map(cb => cb.value);

        if (selectedIds.length === 0) {
            alert('Выберите элементы для удаления');
            return;
        }

        if (confirm('Вы уверены, что хотите удалить выбранные элементы?')) {
            fetch('/vehicles/bulk-delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ ids: selectedIds }),
                credentials: 'same-origin'
            })
            .then(response => response.json())
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

    // Инициализация начального состояния
    updateBulkActionsVisibility();
});