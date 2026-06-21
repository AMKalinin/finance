#!/bin/bash
# Скрипт для инициализации базы данных с тестовыми данными

echo "🚀 Инициализация базы данных Finance Backend..."

# Проверка, что скрипт запускается из правильного каталога
if [ ! -f "/home/alex/Documents/finance/backend/app/core/config.py" ]; then
    echo "❌ Ошибка: Не найден конфигурационный файл!"
    exit 1
fi

echo ""
echo "📝 Шаг 1: Заполнение базы тестовыми данными..."
echo ""

# Запуск скрипта заполнения данных
cd /home/alex/Documents/finance/backend/app
poetry run python scripts/seed_sample_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ База данных успешно заполнена!"
    echo ""
    echo "📊 Созданные тестовые данные:"
    echo "   • 4 счета (Сбербанк, Тинькофф, American Express, Кредитная карта)"
    echo "   • 5 категорий расходов + подкатегории"
    echo "   • 3 категории доходов"
else
    echo ""
    echo "❌ Ошибка при заполнении базы данных!"
    exit 1
fi

echo ""
echo "🎉 Готово! Вы можете:"
echo "   1. Запустить фронтенд: cd /home/alex/Documents/finance/frontend && npm run dev"
echo "   2. Создать транзакцию - в полях 'Счет' и 'Категория' появятся реальные данные из БД"
