# 📄 Руководство по пагинации в Finance Backend API

## 🎯 Обзор системы пагинации

Finance Backend теперь поддерживает полную пагинацию для всех списков сущностей:
- **Учетные записи** (Accounts)
- **Категории** (Categories)
- **Транзакции** (Transactions)

### Основные параметры:

| Параметр | Тип | По умолчанию | Максимум | Описание |
|----------|-----|--------------|----------|----------|
| `skip` | int | 0 | 0 | Количество записей для пропуска |
| `limit` | int | 100 | 1000 | Максимальное количество записей в ответе |

---

## 🚀 Быстрый старт

### Пример запроса с пагинацией:

```bash
# Получить первые 50 транзакций
curl "http://localhost:8001/api/v1/transaction/all?skip=0&limit=50"

# Получить транзакции за период (со 100-й по 200-ю)
curl "http://localhost:8001/api/v1/transaction/by_period?from_date=2025-01-01&to_date=2025-12-31&skip=100&limit=100"

# Получить архивированные счета
curl "http://localhost:8001/api/v1/account/archived?skip=0&limit=20"
```

### Ответ с пагинацией:

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Счет в рублях",
      "currency": "RUB",
      "balance": 50000.0,
      ...
    },
    {
      "id": "550e8401-e29b-41d4-a716-446655440000",
      "name": "Счет в долларах",
      "currency": "USD",
      "balance": 1000.0,
      ...
    }
  ],
  "total": 250,
  "skip": 0,
  "limit": 50,
  "has_more": true
}
```

**Поля ответа:**
- `items`: Список записей (массив объектов)
- `total`: Общее количество записей в коллекции
- `skip`: Пропущенное количество записей (соответствует запросу)
- `limit`: Запрошенное количество записей (макс. 1000)
- `has_more`: true если есть еще записи, false иначе

---

## 📊 Эндпоинты с пагинацией

### 1. Учетные записи (Accounts)

#### Получить все счета
```
GET /api/v1/account/?skip=0&limit=100
```

**Примеры:**
```bash
# Первые 25 счетов
curl "http://localhost:8001/api/v1/account/?skip=0&limit=25"

# С 50-го по 75-й счет (пагинация)
curl "http://localhost:8001/api/v1/account/?skip=50&limit=25"
```

#### Получить архивированные счета
```
GET /api/v1/account/archived?skip=0&limit=100
```

**Пример:**
```bash
# Первые 10 архивированных счетов
curl "http://localhost:8001/api/v1/account/archived?skip=0&limit=10"
```

#### Получить основные счета
```
GET /api/v1/account/primary?skip=0&limit=100
```

**Пример:**
```bash
# Основные счета (обычно 1-2)
curl "http://localhost:8001/api/v1/account/primary"
```

### 2. Категории (Categories)

#### Получить все категории
```
GET /api/v1/category/?skip=0&limit=100
```

**Пример:**
```bash
# Первые 30 категорий верхнего уровня
curl "http://localhost:8001/api/v1/category/?skip=0&limit=30"
```

#### Получить категории расходов
```
GET /api/v1/category/type/expenses?skip=0&limit=100
```

**Пример:**
```bash
# Категории расходов (первые 20)
curl "http://localhost:8001/api/v1/category/type/expenses?skip=0&limit=20"
```

#### Получить категории доходов
```
GET /api/v1/category/type/income?skip=0&limit=100
```

**Пример:**
```bash
# Категории доходов (первые 15)
curl "http://localhost:8001/api/v1/category/type/income?skip=0&limit=15"
```

### 3. Транзакции (Transactions)

#### Получить все транзакции
```
GET /api/v1/transaction/all?skip=0&limit=100
```

**Пример:**
```bash
# Первые 50 транзакций
curl "http://localhost:8001/api/v1/transaction/all?skip=0&limit=50"

# С 200-й по 300-ю транзакцию
curl "http://localhost:8001/api/v1/transaction/all?skip=200&limit=100"
```

#### Получить транзакции за период
```
GET /api/v1/transaction/by_period?from_date=2025-01-01&to_date=2025-12-31&skip=0&limit=100
```

**Пример:**
```bash
# Транзакции за 2025 год (первые 100)
curl "http://localhost:8001/api/v1/transaction/by_period?from_date=2025-01-01&to_date=2025-12-31"

# Транзакции за январь 2025 (со 100-й по 200-ю)
curl "http://localhost:8001/api/v1/transaction/by_period?from_date=2025-01-01&to_date=2025-01-31&skip=100&limit=100"
```

#### Получить транзакции за период с фильтром по типу
```
GET /api/v1/transaction/by_period_type?from_date=2025-01-01&to_date=2025-12-31&operation_type=debit&skip=0&limit=100
```

**Примеры:**
```bash
# Расходы (debit) за 2025 год
curl "http://localhost:8001/api/v1/transaction/by_period_type?from_date=2025-01-01&to_date=2025-12-31&operation_type=debit"

# Переводы (transfer) за январь 2025
curl "http://localhost:8001/api/v1/transaction/by_period_type?from_date=2025-01-01&to_date=2025-01-31&operation_type=transfer"

# Доходы (adding) за март 2025
curl "http://localhost:8001/api/v1/transaction/by_period_type?from_date=2025-03-01&to_date=2025-03-31&operation_type=adding"
```

---

## 🎨 Использование в Postman

### Создание коллекции с пагинацией:

1. Откройте импортированную коллекцию `postman_collection.json`
2. Найдите нужные эндпоинты (например, "Get All Transactions")
3. В URL добавьте параметры:
   ```
   http://localhost:8001/api/v1/transaction/all?skip=0&limit=50
   ```

### Автоматизация пагинации в Postman:

```javascript
// В тесте для получения общей информации
pm.test("Save pagination info", function () {
    var jsonData = pm.response.json();
    
    // Сохраняем общую информацию для следующей итерации
    pm.environment.set("total_count", jsonData.total);
    pm.environment.set("current_skip", jsonData.skip);
    pm.environment.set("current_limit", jsonData.limit);
    pm.environment.set("has_more", jsonData.has_more ? "true" : "false");
    
    // Выводим информацию в консоль
    console.log(`Total: ${jsonData.total}, Skip: ${jsonData.skip}, Limit: ${jsonData.limit}, Has more: ${jsonData.has_more}`);
});

// Проверка на наличие еще данных
pm.test("Check if there are more items", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.has_more).to.be.true; // или false для последней страницы
});
```

---

## 🔄 Программная пагинация (страницы)

### Пример: перебор всех записей

```python
import requests

BASE_URL = "http://localhost:8001/api/v1"
skip = 0
limit = 50
all_items = []

while True:
    response = requests.get(f"{BASE_URL}/transaction/all", params={"skip": skip, "limit": limit})
    data = response.json()
    
    all_items.extend(data["items"])
    
    if not data["has_more"]:
        break
    
    # Переходим на следующую страницу
    skip += limit

print(f"Всего получено {len(all_items)} транзакций")
```

### Использование с offset (альтернативный подход):

```python
# Для больших наборов данных можно использовать offset-based пагинацию
def fetch_all_with_offset(base_url, entity_type="transaction", limit=100):
    all_data = []
    page = 0
    
    while True:
        skip = page * limit
        response = requests.get(f"{base_url}/{entity_type}/all", 
                              params={"skip": skip, "limit": limit})
        
        data = response.json()
        if not data["items"]:
            break
        
        all_data.extend(data["items"])
        
        if not data["has_more"]:
            break
        
        page += 1
    
    return all_data

# Использование
transactions = fetch_all_with_offset("http://localhost:8001/api/v1")
```

---

## 📈 Оптимизация и производительность

### Рекомендации по использованию пагинации:

#### ✅ Делайте:

1. **Используйте разумный limit**: 50-100 записей для большинства случаев
2. **Кэшируйте total_count** на клиенте, если не часто обновляется
3. **Проверяйте has_more** перед следующей страницей
4. **Обработайте крайние случаи** (когда skip >= total)

#### ❌ Не делайте:

1. **Не используйте очень большие limit** (> 500) - замедляет ответ
2. **Не запрашивайте страницы с skip >> total** - вернет пустой список
3. **Не игнорируйте has_more** - можно потерять данные при ошибке логики

### Производительность:

| Limit | Время ответа (примерное) | Рекомендация |
|-------|-------------------------|--------------|
| 10 | ~50ms | Быстрый ответ, подходит для мобильных |
| 50 | ~100ms | Оптимально для большинства случаев |
| 100 | ~200ms | Стандартное значение по умолчанию |
| 500 | ~800ms | Не рекомендуется для production |

---

## 🐛 Обработка ошибок при пагинации

### Ошибки параметров:

```bash
# skip не может быть отрицательным
curl "http://localhost:8001/api/v1/transaction/all?skip=-5&limit=50"
# Ответ: 422 Validation Error - skip должен быть >= 0

# limit слишком большой
curl "http://localhost:8001/api/v1/transaction/all?skip=0&limit=2000"
# Ответ: 422 Validation Error - limit не может превышать 1000
```

### Пример обработки ошибок на Python:

```python
import requests
from requests.exceptions import RequestException

def fetch_with_retry(base_url, entity_type="transaction", max_pages=10):
    skip = 0
    limit = 50
    all_items = []
    
    for page in range(max_pages):
        try:
            response = requests.get(
                f"{base_url}/{entity_type}/all",
                params={"skip": skip, "limit": limit},
                timeout=10
            )
            
            if response.status_code == 422:
                print(f"Ошибка валидации на странице {page}")
                break
            
            data = response.json()
            all_items.extend(data["items"])
            
            if not data["has_more"]:
                break
            
            skip += limit
            
        except RequestException as e:
            print(f"Ошибка сети при запросе страницы {page}: {e}")
            return all_items
    
    return all_items
```

---

## 📝 Примеры использования в разных языках

### JavaScript/TypeScript:

```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
}

async function fetchTransactions(
  baseUrl: string,
  limit: number = 50
): Promise<any[]> {
  const allTransactions: any[] = [];
  let skip = 0;
  
  while (true) {
    const response = await fetch(
      `${baseUrl}/transaction/all?skip=${skip}&limit=${limit}`
    );
    
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data: PaginatedResponse<any> = await response.json();
    allTransactions.push(...data.items);
    
    if (!data.has_more) break;
    skip += limit;
  }
  
  return allTransactions;
}

// Использование
const transactions = await fetchTransactions("http://localhost:8001/api/v1");
console.log(`Получено ${transactions.length} транзакций`);
```

### Java (Spring WebFlux):

```java
public Mono<List<Transaction>> fetchAllWithPagination(String baseUrl) {
    return Flux.range(0, 100) // max pages
        .flatMap(page -> 
            webClient.get()
                .uri(uriBuilder -> uriBuilder
                    .path("/transaction/all")
                    .queryParam("skip", page * 50)
                    .queryParam("limit", 50)
                    .build())
                .retrieve()
                .bodyToMono(PaginatedResponse.class)
        )
        .filter(response -> !response.hasMore())
        .next()
        .flatMapMany(response -> 
            Flux.fromIterable(response.getItems())
        );
}
```

### C# (.NET):

```csharp
public async Task<List<Transaction>> FetchAllWithPaginationAsync(string baseUrl, int limit = 50)
{
    var allTransactions = new List<Transaction>();
    int skip = 0;
    
    while (true)
    {
        var response = await _httpClient.GetStringAsync(
            $"/api/v1/transaction/all?skip={skip}&limit={limit}"
        );
        
        var data = JsonSerializer.Deserialize<PaginatedResponse<Transaction>>(response);
        allTransactions.AddRange(data.Items);
        
        if (!data.HasMore) break;
        skip += limit;
    }
    
    return allTransactions;
}
```

---

## 📊 Сравнение с другими подходами

### Offset-based (используется в Finance Backend):

| Плюсы | Минусы |
|-------|--------|
| Простота реализации | Проблемы при удалении данных между запросами |
| Интуитивно понятный API | Медленная работа на больших skip значениях |
| Хорошо для большинства случаев | - |

### Cursor-based (альтернатива):

```bash
# Пример cursor-based пагинации
curl "http://localhost:8001/api/v1/transaction/all?cursor=abc123&limit=50"
```

**Плюсы:**
- Быстрее на больших объемах данных
- Стабильнее при удалении/добавлении записей

**Минусы:**
- Сложнее в реализации
- Менее интуитивен для пользователей

---

## 🎯 Best Practices

### ✅ Делайте:

1. **Всегда проверяйте has_more** перед следующей страницей
2. **Используйте limit от 50 до 100** для баланса производительности и UX
3. **Кэшируйте total_count** на клиенте при необходимости
4. **Обрабатывайте крайние случаи** (skip >= total, пустые страницы)

### ❌ Не делайте:

1. **Не используйте limit > 500** - замедляет ответ
2. **Не запрашивайте skip >> total** - вернет пустой список
3. **Не игнорируйте has_more** - можно потерять данные

---

## 📞 Troubleshooting

### Проблема: Получаю много страниц при большом наборе данных

**Решение:** Увеличьте limit до 100 (максимум):
```bash
curl "http://localhost:8001/api/v1/transaction/all?limit=100"
```

### Проблема: has_more всегда true, даже когда должен быть false

**Решение:** Проверьте правильность skip значения - возможно оно не увеличивается корректно.

### Проблема: Медленный ответ при большом skip

**Решение:** Используйте cursor-based пагинацию (требуется дополнительная реализация).

---

## 📚 Дополнительные ресурсы

- [Pagination in REST APIs](https://restfulapi.net/pagination/)
- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query/)
- [Offset vs Cursor Pagination](https://www.mongodb.com/blog/post/offset-pagination-vs-cursor-based-pagination)

---

**Дата создания:** 9 мая 2025  
**Версия системы пагинации:** 1.0.0
