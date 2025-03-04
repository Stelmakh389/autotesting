// Функция сохранения ширины колонок
function saveColumnWidths() {
    const table = document.getElementById('overflowSample');
    const headers = table.querySelectorAll('th');
    const widths = {};
    
    headers.forEach((header, index) => {
        if (index > 1) { // Пропускаем чекбокс и номер
            const columnKey = `column_${index}`;
            const width = header.offsetWidth;
            widths[columnKey] = width;
            console.log(`Сохраняем ширину для колонки ${columnKey}: ${width}px`);
        }
    });
    
    localStorage.setItem('columnWidths', JSON.stringify(widths));
    console.log('Сохранено в localStorage:', widths);
}

// Функция загрузки и применения сохраненных настроек
function loadColumnWidths() {
    const savedWidths = localStorage.getItem('columnWidths');
    console.log('Загружено из localStorage:', savedWidths);
    
    if (savedWidths) {
        const widths = JSON.parse(savedWidths);
        const table = document.getElementById('overflowSample');
        const headers = table.querySelectorAll('th');
        
        headers.forEach((header, index) => {
            if (index > 1) {
                const columnKey = `column_${index}`;
                if (widths[columnKey]) {
                    header.style.width = `${widths[columnKey]}px`;
                    console.log(`Установлена ширина для колонки ${columnKey}: ${widths[columnKey]}px`);
                }
            }
        });
    }
}

// Инициализация colResizable с сохранением
function initializeColResizable() {
    $("#overflowSample").colResizable({
        disable: true  // Сначала отключаем, если уже было инициализировано
    });
    
    $("#overflowSample").colResizable({
        resizeMode: 'overflow',
        onResize: function() {
            console.log('onResize triggered');
            saveColumnWidths();
        },
        postbackSafe: true,
        partialRefresh: true
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, начинаем инициализацию');
    
    // Загружаем сохраненные настройки
    loadColumnWidths();
    
    // Инициализируем colResizable
    setTimeout(() => {
        initializeColResizable();
        console.log('colResizable инициализирован');
    }, 100);
    
    // Инициализация модального окна удаления
    const modalElement = document.getElementById('deleteConfirmationModal');
    if (modalElement) {
        window.deleteModal = new bootstrap.Modal(modalElement);
    }
});

// Добавляем обработчик на случай динамической перезагрузки таблицы
const observer = new MutationObserver(() => {
    initializeColResizable();
    loadColumnWidths();
});

observer.observe(document.getElementById('overflowSample'), {
    childList: true,
    subtree: true
});