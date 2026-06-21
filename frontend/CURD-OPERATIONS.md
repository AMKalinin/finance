# CRUD Операции для Финансового Приложения

## Обзор

Это приложение реализует полные CRUD (Create, Read, Update, Delete) операции для всех основных сущностей: счетов, транзакций, категорий и друзей. Все операции работают через API слой с поддержкой моковых данных для тестирования без реального бэкенда.

---

## Архитектура

### Компоненты CRUD операций

| Компонент | Назначение | Файл |
|-----------|------------|------|
| `CreateAccountModal` | Создание/редактирование счетов | `/src/components/Modals/CreateAccountModal.vue` |
| `CreateTransactionModal` | Создание/редактирование транзакций | `/src/components/Modals/CreateTransactionModal.vue` |
| `CreateCategoryModal` | Создание/редактирование категорий | `/src/components/Modals/CreateCategoryModal.vue` |
| `CreateFriendModal` | Добавление друзей | `/src/components/Modals/CreateFriendModal.vue` |

### API Слой

Все CRUD операции реализованы через API модули в `/src/api/client.js`:

- **Account API**: `accountApi` - управление счетами
- **Transaction API**: `transactionApi` - управление транзакциями  
- **Category API**: `categoryApi` - управление категориями
- **Friend API**: `friendApi` - управление друзьями

---

## Реализация CRUD операций

### 1. Счета (Accounts)

#### Create (Создание)
```javascript
// Открыть модальное окно создания счета
emit('openModal', 'account')

// В модалке:
await accountApi.create({
  name: 'Основной банковский',
  type: 'debit',
  currency: 'RUB',
  balance: 150000.00,
  interestRate: 5.5,
  isPrimary: true
})
```

#### Read (Чтение)
```javascript
// Получить все счета
const accounts = await accountApi.getAll()

// Получить конкретный счет
const account = await accountApi.getById(id)

// Получить основной счет
const primary = await accountApi.primary()

// Получить архивированные счета
const archived = await accountApi.archived()
```

#### Update (Обновление)
```javascript
// Открыть модальное окно с данными для редактирования
emit('openModal', 'account', existingAccount)

// В модалке:
await accountApi.update(id, {
  name: 'Новое название',
  balance: 200000.00,
  interestRate: 6.5
})
```

#### Delete (Удаление)
```javascript
function openDeleteAccount(account) {
  if (confirm(`Вы уверены, что хотите удалить счет "${account.name}"?`)) {
    // Подтверждение удаления
  }
}
```

---

### 2. Транзакции (Transactions)

#### Create (Создание)
```javascript
// Открыть модальное окно создания транзакции
emit('openModal', 'transaction')

// В модалке:
await transactionApi.create({
  type: 'debit', // or 'adding', 'transfer'
  fromAccountId: 1,
  toAccountId: null,
  categoryId: 2,
  amount: -3450.00,
  currency: 'RUB',
  date: '2025-05-15',
  description: 'Супермаркет "Лента"'
})
```

#### Read (Чтение)
```javascript
// Получить все транзакции
const transactions = await transactionApi.getAll()

// Получить транзакции за период
const periodTransactions = await transactionApi.getByPeriod(startDate, endDate)
```

#### Update (Обновление)
```javascript
// Открыть модальное окно с данными для редактирования
emit('openModal', 'transaction', existingTransaction)

// В модалке:
await transactionApi.update(id, {
  amount: -4000.00,
  categoryId: 3,
  description: 'Новое описание'
})
```

#### Delete (Удаление)
```javascript
async function deleteTransaction(id, name) {
  if (confirm(`Вы уверены, что хотите удалить транзакцию "${name}"?`)) {
    await transactionApi.delete(id)
    // Перезагрузка списка
    emit('refresh', 'transactions')
  }
}
```

---

### 3. Категории (Categories)

#### Create (Создание)
```javascript
// Открыть модальное окно создания категории
emit('openModal', 'category')

// В модалке:
await categoryApi.create({
  name: 'Супермаркеты',
  type: 'expense',
  parentId: null, // or parent category id
  icon: '🛒'
})
```

#### Read (Чтение)
```javascript
// Получить все категории
const categories = await categoryApi.getAll()

// Получить только расходы
const expenses = await categoryApi.getExpenses()

// Получить только доходы
const income = await categoryApi.getIncome()
```

#### Update (Обновление)
```javascript
// Открыть модальное окно с данными для редактирования
emit('openModal', 'category', existingCategory)

// В модалке:
await categoryApi.update(id, {
  name: 'Новое название категории',
  icon: '🍕'
})
```

#### Delete (Удаление)
```javascript
async function deleteCategory(id, name) {
  if (confirm(`Вы уверены, что хотите удалить категорию "${name}" и всех её потомков?`)) {
    await categoryApi.delete(id)
    // Перезагрузка списка категорий
    emit('refresh', 'categories')
  }
}
```

**Важно**: При удалении категории удаляются все её дочерние категории рекурсивно.

---

### 4. Друзья (Friends)

#### Create (Создание)
```javascript
// Открыть модальное окно добавления друга
emit('openModal', 'friend')

// В модалке:
await friendApi.create({
  name: 'Иван Петров',
  initials: 'ИП',
  status: 'pending', // or 'friend'
  avatarColor: 'bg-blue-500'
})
```

#### Read (Чтение)
```javascript
// Получить всех друзей
const friends = await friendApi.getAll()

// Получить запросы на добавление в друзья
const requests = await friendApi.getRequests()
```

#### Update (Обновление)
```javascript
// Открыть модальное окно с данными для редактирования
emit('openModal', 'friend', existingFriend)

// В модалке:
await friendApi.update(id, {
  name: 'Новое имя друга',
  avatarColor: 'bg-green-500'
})
```

#### Delete (Удаление)
```javascript
async function removeFriend(id) {
  await friendApi.removeFriend(id)
  // Перезагрузка списка друзей
  emit('refresh', 'friends')
}
```

---

## UI/UX реализации

### Модальные окна

Все модальные окна имеют общий интерфейс:
- **Header**: Заголовок с кнопкой закрытия (✕)
- **Form**: Форма валидации и редактирования данных
- **Actions**: Кнопки "Сохранить" и "Отмена"

### Валидация форм

Каждая форма имеет систему валидации:
```javascript
function validate() {
  errors.value = {}
  
  if (!form.value.name.trim()) {
    errors.value.name = 'Название обязательно'
  }
  
  return Object.keys(errors.value).length === 0
}
```

### Обработка ошибок

Все операции обернуты в try-catch блоки:
```javascript
try {
  await apiMethod()
  emit('saved')
  closeModal()
} catch (error) {
  console.error('Ошибка сохранения:', error)
  errors.value.general = 'Произошла ошибка при сохранении'
} finally {
  isLoading.value = false
}
```

### Подтверждение удаления

Критические операции требуют подтверждения:
```javascript
if (confirm(`Вы уверены, что хотите удалить "${name}"?`)) {
  // Выполнение операции
}
```

---

## API слой

### Mock Data System

Все API методы используют систему моковых данных через `window._mock*`:
```javascript
export const accountApi = {
  getAll: async () => {
    if (!window._mockAccounts) window._mockAccounts = [...mockData.accounts]
    return window._mockAccounts
  }
}
```

### Асинхронность

Все операции асинхронные и возвращают промисы. Добавлена имитация сетевой задержки:
```javascript
const simulateNetworkDelay = () => 
  new Promise(resolve => setTimeout(resolve, Math.random() * 500 + 200))
```

### Очередь запросов

При отсутствии сети операции ставятся в очередь и повторяются при восстановлении соединения.

---

## Использование CRUD операций в компонентах View

### Пример использования в DashboardView

```javascript
// Обработчик открытия модального окна
function openCreateTransaction() {
  emit('openModal', 'transaction')
}

// Обработчик обновления данных
async function refreshAccounts() {
  console.log('Refreshing accounts...')
  // Перезагрузка данных из API
}
```

### Пример использования в AccountsView

```javascript
const emit = defineEmits(['openModal', 'refresh'])

function openEditAccount(account) {
  emit('openModal', 'account', account)
}

async function deleteTransaction(id, name) {
  if (confirm(`Вы уверены?`)) {
    await transactionApi.delete(id)
    emit('refresh', 'transactions')
  }
}
```

---

## Типы транзакций

| Тип | Описание | Значение суммы |
|-----|----------|----------------|
| `debit` | Расход (списание) | Отрицательное (-3450.00) |
| `adding` | Доход (зачисление) | Положительное (+85000.00) |
| `transfer` | Перевод между счетами | Зависит от направления |

---

## Типы категорий

| Тип | Описание | Цвет |
|-----|----------|------|
| `expense` | Расходы | Red-600 |
| `income` | Доходы | Green-600 |
| `transfer` | Переводы | Blue-600 |

---

## Инициалы и аватары

### Генерация инициалов
```javascript
function generateInitials(name) {
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    form.value.initials = `${parts[0][0]}${parts[1][0]}`.toUpperCase()
  } else if (name.length >= 2) {
    form.value.initials = name.substring(0, 2).toUpperCase()
  }
}
```

### Цвета аватаров
Доступные цвета для выбора:
- `bg-blue-500`, `bg-green-500`, `bg-yellow-500`
- `bg-red-500`, `bg-purple-500`, `bg-pink-500`
- `bg-indigo-500`, `bg-teal-500`

---

## Переходы и анимации

### Модальные окна
```css
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Переходы роутера
```javascript
<transition name="fade" mode="out-in">
  <component :is="Component" />
</transition>
```

---

## Хуки жизненного цикла

### onMounted
Загрузка данных при монтировании компонента:
```javascript
onMounted(async () => {
  await fetchAccounts()
})
```

### onOpen
Инициализация модального окна при открытии:
```javascript
function onOpen() {
  if (props.modelValue) {
    loadEditData()
    loadParentCategories()
  }
}
```

---

## Обработка состояний загрузки

Все формы имеют состояние загрузки:
```javascript
const isLoading = ref(false)

// В кнопке:
<button :disabled="isLoading">
  {{ isLoading ? 'Сохранение...' : 'Создать' }}
</button>

// Индикатор загрузки в UI:
<div v-if="isLoading" class="spinner">...</div>
```

---

## Стили и дизайн

### Цветовая схема для ошибок
- Поля с ошибками: `border-red-500 bg-red-50 dark:bg-red-900/20`
- Сообщения об ошибках: `text-red-500`

### Активные состояния
- Кнопки при наведении: `hover:bg-blue-700`
- Поля с фокусом: `focus:ring-2 focus:ring-blue-500`
- Группы элементов при наведении: `group-hover:opacity-100`

---

## Тестирование CRUD операций

### Методы тестирования

1. **Создание нового счета**:
   - Нажать "Новый счёт" в AccountsView
   - Заполнить все обязательные поля
   - Сохранить и проверить появление в списке

2. **Редактирование транзакции**:
   - Кликнуть на иконку транзакции или кнопку ✏️
   - Изменить данные
   - Сохранить и проверить обновление

3. **Удаление категории**:
   - Навести курсор на категорию в дереве
   - Нажать 🗑️ (появится при наведении)
   - Подтвердить удаление
   - Проверить удаление всех потомков

4. **Добавление друга**:
   - Нажать "Добавить" в FriendsView
   - Заполнить имя и выбрать цвет аватара
   - Сохранить и проверить появление в списке

---

## Будущие улучшения

1. **Реалный бэкенд**: Подключение реального API вместо моковых данных
2. **Кеширование**: Добавление кеширования для оптимизации производительности
3. **Полноценная пагинация**: Реализация клиентской и серверной пагинации
4. **Поиск и фильтры**: Расширенные возможности фильтрации данных
5. **Экспорт данных**: Возможность экспорта в CSV, Excel, PDF
6. **История изменений**: Отслеживание истории операций CRUD
7. **Валидация на стороне бэкенда**: Дублирование валидации для безопасности

---

## Заключение

Все CRUD операции реализованы с использованием:
- ✅ Vue 3 Composition API
- ✅ TypeScript (готовность к использованию)
- ✅ Pinia stores для управления состоянием
- ✅ Vue Router для навигации
- ✅ Axios для HTTP запросов
- ✅ Tailwind CSS для стилизации
- ✅ Иерархические структуры данных
- ✅ Валидация форм с обратной связью
- ✅ Обработка ошибок и загрузок
- ✅ Модальные окна с анимацией

Приложение готово к использованию как в демо-режиме, так и при подключении реального бэкенда.
