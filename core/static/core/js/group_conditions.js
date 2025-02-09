// static/js/group_conditions.js
document.addEventListener('DOMContentLoaded', function() {
    // Определение типов полей и их возможных операторов
    const fieldTypes = {
        'engine_volume': {
            type: 'numeric',
            label: 'Объем двигателя',
            operators: ['=', '>=', '<=']
        },
        'engine_power': {
            type: 'numeric',
            label: 'Мощность двигателя',
            operators: ['=', '>=', '<=']
        },
        'fuel_type': {
            type: 'select',
            label: 'Тип топлива',
            options: [
                {value: 'gasoline', label: 'Бензин'},
                {value: 'diesel', label: 'Дизель'},
                {value: 'gas', label: 'Газ'},
                {value: 'electric', label: 'Электро'},
                {value: 'hybrid', label: 'Гибрид'}
            ]
        },
        'max_mass': {
            type: 'numeric',
            label: 'Максимальная масса',
            operators: ['=', '>=', '<=']
        },
        'unladen_mass': {
            type: 'numeric',
            label: 'Масса без нагрузки',
            operators: ['=', '>=', '<=']
        }
    };

    // Контейнер для условий
    const conditionsContainer = document.getElementById('conditions-container');
    const addConditionBtn = document.getElementById('add-condition-btn');
    const conditionsInput = document.getElementById('id_conditions');
    
    let conditions = [];
    try {
        conditions = JSON.parse(conditionsInput.value || '[]');
    } catch (e) {
        conditions = [];
    }

    // Функция создания HTML для условия
    function createConditionHTML(condition = null, index) {
        const div = document.createElement('div');
        div.className = 'condition-row mb-3 p-3 border rounded';
        div.dataset.index = index;

        // Выбор поля
        let fieldSelect = document.createElement('select');
        fieldSelect.className = 'form-select field-select mb-2';
        fieldSelect.innerHTML = `<option value="">Выберите поле</option>`;
        Object.keys(fieldTypes).forEach(field => {
            fieldSelect.innerHTML += `<option value="${field}" ${condition && condition.field === field ? 'selected' : ''}>
                ${fieldTypes[field].label}
            </option>`;
        });

        // Контейнер для операторов и значений (будет заполнен позже)
        const operatorValueContainer = document.createElement('div');
        operatorValueContainer.className = 'operator-value-container';

        // Кнопка удаления
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn btn-danger mt-2';
        removeBtn.innerHTML = 'Удалить условие';
        removeBtn.onclick = function() {
            div.remove();
            updateConditions();
        };

        div.appendChild(fieldSelect);
        div.appendChild(operatorValueContainer);
        div.appendChild(removeBtn);

        // Если есть существующее условие, заполняем операторы и значения
        if (condition) {
            updateOperatorValue(operatorValueContainer, condition.field, condition);
        }

        // Обработчик изменения поля
        fieldSelect.onchange = function() {
            updateOperatorValue(operatorValueContainer, this.value);
        };

        return div;
    }

    // Функция обновления операторов и значений
    function updateOperatorValue(container, fieldName, condition = null) {
        if (!fieldName || !fieldTypes[fieldName]) {
            container.innerHTML = '';
            return;
        }

        const fieldInfo = fieldTypes[fieldName];
        container.innerHTML = '';

        if (fieldInfo.type === 'numeric') {
            // Селект для операторов
            const operatorSelect = document.createElement('select');
            operatorSelect.className = 'form-select operator-select mb-2';
            fieldInfo.operators.forEach(op => {
                operatorSelect.innerHTML += `<option value="${op}" ${condition && condition.operator === op ? 'selected' : ''}>
                    ${op}
                </option>`;
            });

            // Поле для значения
            const valueInput = document.createElement('input');
            valueInput.type = 'number';
            valueInput.className = 'form-control value-input';
            valueInput.step = '0.1';
            if (condition) valueInput.value = condition.value;

            container.appendChild(operatorSelect);
            container.appendChild(valueInput);

        } else if (fieldInfo.type === 'select') {
            // Селект для значений
            const valueSelect = document.createElement('select');
            valueSelect.className = 'form-select value-select';
            fieldInfo.options.forEach(option => {
                valueSelect.innerHTML += `<option value="${option.value}" ${condition && condition.value === option.value ? 'selected' : ''}>
                    ${option.label}
                </option>`;
            });

            container.appendChild(valueSelect);
        }

        // При любом изменении обновляем общий список условий
        container.querySelectorAll('select, input').forEach(el => {
            el.onchange = updateConditions;
        });
    }

    // Функция обновления всех условий
    function updateConditions() {
        const conditions = [];
        document.querySelectorAll('.condition-row').forEach(row => {
            const fieldSelect = row.querySelector('.field-select');
            const field = fieldSelect.value;
            
            if (field && fieldTypes[field]) {
                let condition = { field };
                
                if (fieldTypes[field].type === 'numeric') {
                    const operatorSelect = row.querySelector('.operator-select');
                    const valueInput = row.querySelector('.value-input');
                    if (operatorSelect && valueInput && valueInput.value) {
                        condition.operator = operatorSelect.value;
                        condition.value = parseFloat(valueInput.value);
                        conditions.push(condition);
                    }
                } else if (fieldTypes[field].type === 'select') {
                    const valueSelect = row.querySelector('.value-select');
                    if (valueSelect) {
                        condition.value = valueSelect.value;
                        conditions.push(condition);
                    }
                }
            }
        });

        conditionsInput.value = JSON.stringify(conditions);
    }

    // Добавление начальных условий
    conditions.forEach((condition, index) => {
        conditionsContainer.appendChild(createConditionHTML(condition, index));
    });

    // Обработчик добавления нового условия
    addConditionBtn.onclick = function() {
        conditionsContainer.appendChild(createConditionHTML(null, conditionsContainer.children.length));
    };
});