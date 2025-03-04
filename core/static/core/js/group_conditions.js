// static/js/group_conditions.js
class ConditionsManager {
    constructor(containerId, inputId, addBtnId, csrfToken) {
        this.container = document.getElementById(containerId);
        this.conditionsInput = document.getElementById(inputId);
        this.addButton = document.getElementById(addBtnId);
        this.csrfToken = csrfToken;
        this.fieldTypes = {};
        
        this.init();
    }

    async init() {
        try {
            console.log('Fetching metadata...');
            const response = await fetch('/api/model-metadata/vehicle/', {
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Читаем JSON только один раз и сохраняем результат
            const data = await response.json();
            console.log('Received metadata:', data);
            
            // Используем полученные данные
            this.fieldTypes = data;
            
            // Показываем UI
            this.container.style.display = 'block';
            this.addButton.style.display = 'block';
            
            // Инициализируем существующие условия
            this.loadExistingConditions();
            
            // Добавляем обработчик для кнопки
            this.addButton.onclick = () => this.addCondition();
            
        } catch (error) {
            console.error('Error details:', error);
            this.showError('Не удалось загрузить метаданные полей. Пожалуйста, обновите страницу.');
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.textContent = message;
        this.container.parentNode.insertBefore(errorDiv, this.container);
    }

    loadExistingConditions() {
        let conditions = [];
        try {
            conditions = JSON.parse(this.conditionsInput.value || '[]');
        } catch (e) {
            conditions = [];
        }

        conditions.forEach((condition, index) => {
            this.addCondition(condition);
        });
    }

    createOperatorSelect(fieldInfo, selectedOperator = null) {
        const select = document.createElement('select');
        select.className = 'form-select operator-select mb-2';
        
        fieldInfo.operators.forEach(op => {
            const option = document.createElement('option');
            option.value = op;
            option.textContent = this.getOperatorLabel(op);
            option.selected = op === selectedOperator;
            select.appendChild(option);
        });

        return select;
    }

    getOperatorLabel(op) {
        const operatorLabels = {
            '=': 'равно',
            '>=': 'больше или равно',
            '<=': 'меньше или равно',
            '>': 'больше',
            '<': 'меньше',
            'contains': 'содержит',
            'startswith': 'начинается с',
            'endswith': 'заканчивается на'
        };
        return operatorLabels[op] || op;
    }

    createValueInput(fieldInfo, currentValue = null) {
        let input;

        switch (fieldInfo.type) {
            case 'select':
                input = document.createElement('select');
                input.className = 'form-select value-select';
                fieldInfo.options.forEach(option => {
                    const opt = document.createElement('option');
                    opt.value = option.value;
                    opt.textContent = option.label;
                    opt.selected = option.value === currentValue;
                    input.appendChild(opt);
                });
                break;

            case 'numeric':
                input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control value-input';
                input.step = '0.1';
                if (currentValue !== null) input.value = currentValue;
                break;

            case 'date':
                input = document.createElement('input');
                input.type = 'date';
                input.className = 'form-control value-input';
                if (currentValue) input.value = currentValue;
                break;

            case 'datetime':
                input = document.createElement('input');
                input.type = 'datetime-local';
                input.className = 'form-control value-input';
                if (currentValue) input.value = currentValue;
                break;

            default:
                input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control value-input';
                if (currentValue) input.value = currentValue;
                break;
        }

        return input;
    }

    createSectionContainer() {
        const section = document.createElement('div');
        section.className = 'condition-section mb-3';
        return section;
    }

    createFieldSelect(condition = null) {
        const section = this.createSectionContainer();
        
        const label = document.createElement('label');
        label.className = 'form-label';
        label.textContent = 'Поле';
        
        const select = document.createElement('select');
        select.className = 'form-select field-select';
        
        const emptyOption = document.createElement('option');
        emptyOption.value = '';
        emptyOption.textContent = 'Выберите поле';
        select.appendChild(emptyOption);

        Object.entries(this.fieldTypes).forEach(([fieldName, fieldInfo]) => {
            const option = document.createElement('option');
            option.value = fieldName;
            option.textContent = fieldInfo.label;
            option.selected = condition && condition.field === fieldName;
            select.appendChild(option);
        });

        section.appendChild(label);
        section.appendChild(select);
        return { section, select };
    }

    addCondition(condition = null) {
        const div = document.createElement('div');
        div.className = 'condition-row mb-3 p-3 border rounded bg-light';

        // Добавляем заголовок условия
        const header = document.createElement('div');
        header.className = 'd-flex justify-content-between align-items-center mb-3';
        
        const title = document.createElement('h5');
        title.className = 'mb-0';
        title.textContent = 'Условие';
        
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn btn-danger btn-sm';
        removeBtn.innerHTML = 'Удалить';
        removeBtn.onclick = () => {
            div.remove();
            this.updateConditions();
        };

        header.appendChild(title);
        header.appendChild(removeBtn);
        div.appendChild(header);

        // Создаем контейнер для полей
        const fieldsContainer = document.createElement('div');
        fieldsContainer.className = 'fields-container';

        // Добавляем выбор поля
        const { section: fieldSection, select: fieldSelect } = this.createFieldSelect(condition);
        fieldsContainer.appendChild(fieldSection);

        // Контейнер для операторов и значений
        const operatorValueContainer = document.createElement('div');
        operatorValueContainer.className = 'operator-value-container mt-3';
        fieldsContainer.appendChild(operatorValueContainer);

        div.appendChild(fieldsContainer);
        this.container.appendChild(div);

        // Если есть существующее условие, заполняем операторы и значения
        if (condition) {
            this.updateOperatorValue(operatorValueContainer, condition.field, condition);
        }

        // Обработчик изменения поля
        fieldSelect.onchange = () => {
            this.updateOperatorValue(operatorValueContainer, fieldSelect.value);
            this.updateConditions();
        };
    }

    updateOperatorValue(container, fieldName, condition = null) {
        if (!fieldName || !this.fieldTypes[fieldName]) {
            container.innerHTML = '';
            return;
        }

        const fieldInfo = this.fieldTypes[fieldName];
        container.innerHTML = '';

        // Создаем селект для операторов (если нужно)
        if (fieldInfo.operators.length > 1) {
            const operatorSelect = this.createOperatorSelect(
                fieldInfo,
                condition ? condition.operator : null
            );
            container.appendChild(operatorSelect);
        }

        // Создаем поле для значения
        const valueInput = this.createValueInput(
            fieldInfo,
            condition ? condition.value : null
        );
        container.appendChild(valueInput);

        // Добавляем обработчики изменений
        container.querySelectorAll('select, input').forEach(el => {
            el.onchange = () => this.updateConditions();
        });
    }

    updateConditions() {
        const conditions = [];
        this.container.querySelectorAll('.condition-row').forEach(row => {
            const fieldSelect = row.querySelector('.field-select');
            const field = fieldSelect.value;
            
            if (field && this.fieldTypes[field]) {
                const condition = { field };
                const operatorSelect = row.querySelector('.operator-select');
                const valueInput = row.querySelector('.value-input, .value-select');
                
                if (operatorSelect) {
                    condition.operator = operatorSelect.value;
                }
                
                if (valueInput && valueInput.value) {  // Убеждаемся, что значение указано
                    condition.value = this.fieldTypes[field].type === 'numeric'
                        ? parseFloat(valueInput.value)
                        : valueInput.value;
                    conditions.push(condition);  // Добавляем только полные условия
                }
            }
        });
        this.conditionsInput.value = JSON.stringify(conditions);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    new ConditionsManager(
        'conditions-container',
        'id_conditions',
        'add-condition-btn'
    );
});