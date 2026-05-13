# Frontend-Backend Integration Summary

This document describes the changes made to align the Vue.js frontend with the FastAPI backend API structure.

## Backend API Structure

### Account Endpoints (`/api/account`)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/` | Get all accounts (paginated) | `skip`, `limit` |
| POST | `/create` | Create new account | Body: account_in schema |
| GET | `/{id}` | Get account by ID | Path: id (UUID) |
| PUT | `/{id}/balance` | Update balance | Body: operation, balance |
| PUT | `/{id}/name` | Update name | Body: name |
| PUT | `/{id}/description` | Update description | Body: description |
| PUT | `/{id}/interest_rate` | Update interest rate | Body: interest_rate |
| PUT | `/{id}/emergency_fund` | Update emergency fund flag | Body: is_emergency_fund |
| PUT | `/{id}/decimal_places` | Update decimal places | Body: decimal_places |
| PUT | `/{id}/archived` | Update archived status | Body: is_archived |
| PUT | `/{id}/primary` | Update primary flag | Body: is_primary |
| GET | `/archived` | Get archived accounts | `skip`, `limit` |
| GET | `/primary` | Get primary accounts | `skip`, `limit` |
| DELETE | `/{id}` | Delete account | Path: id (UUID) |

### Category Endpoints (`/api/category`)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/` | Get all categories (paginated) | `skip`, `limit` |
| POST | `/create` | Create new category | Body: name, type, parentCategory, level |
| PUT | `/{id}/name` | Update category name | Body: name |
| GET | `/type/expenses` | Get expense categories (Debit) | `skip`, `limit` |
| GET | `/type/income` | Get income categories (Credit) | `skip`, `limit` |
| DELETE | `/{id}` | Delete category | Path: id (UUID) |

### Transaction Endpoints (`/api/transaction`)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/all` | Get all transactions (paginated) | `skip`, `limit` |
| GET | `/by_period` | Transactions by date range | `from_date`, `to_date`, `skip`, `limit` |
| GET | `/by_period_type` | Transactions with type filter | `from_date`, `to_date`, `operation_type`, `skip`, `limit` |
| POST | `/create` | Create new transaction | Body: transaction_in schema |
| POST | `/distribution` | Add distribution to transaction | Body: distribution_in schema |
| PATCH | `/distribution` | Update distribution | Body: distribution_in schema |
| DELETE | `/distribution` | Delete distribution | Body: distribution_in schema |
| PATCH | `/distribution/settle` | Settle a distribution | Body: settle_info |
| POST | `/position` | Add position to transaction | Body: position_in schema |
| PATCH | `/position` | Update position | Body: position_in schema |
| PUT | `/{id}/date` | Update transaction date | Body: date |
| PUT | `/{id}/size` | Update transaction size | Body: size |
| PUT | `/{id}/description` | Update description | Body: description |
| DELETE | `/{id}` | Delete transaction | Path: id (UUID) |

### User Endpoints (`/api/user`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/info` | Get user information |
| GET | `/friends` | Get friends list |
| POST | `/friend` | Add friend by ID |
| PUT | `/friend/accept` | Accept friend request |
| PUT | `/friend/reject` | Reject friend request |
| DELETE | `/friend` | Delete friend relationship |

## Frontend Changes Made

### 1. API Service (`src/api/finApi.js`)

**Added Pagination Support:**
- All GET endpoints now support `skip` and `limit` parameters
- Response structure expects `{ items, total, skip, limit, has_more }`

**New Endpoints Added:**
- `getExpenseCategories()` - Get expense (Debit) categories
- `getIncomeCategories()` - Get income (Credit) categories  
- `getPrimaryAccounts()` - Get primary accounts
- `getArchivedAccounts()` - Get archived accounts
- `getTransactionsByPeriod()` - Transactions by date range
- `updateAccount*()` methods for individual account updates
- `deleteAccount()` - Delete an account

**Updated Field Names:**
- Category: `typeCategory` → `type` (Debit/Credit)
- Transaction: `typeName` → `type`, `size` → `debitSize`

### 2. Account Component (`src/components/TopAccounts.vue`)

**Changes:**
- Updated account creation to use backend field names
- Removed hardcoded currency selection logic
- Simplified balance handling

### 3. Category Component (`src/components/TopCategories.vue`)

**Changes:**
- Fixed category type filtering (Debit/Credit)
- Added computed properties for reactive filtering
- Updated delete handler to accept UUID string instead of object

### 4. Transaction Component (`src/components/TransactionTable.vue`)

**Major Changes:**
- Updated field names: `typeName` → `type`, `size` → `debitSize`
- Fixed category filtering logic
- Added support for new transaction structure with distributions and positions
- Updated account/category lookup functions to work with UUIDs

### 5. Chart Components

**PortfolioChart.vue:**
- Updated currency display from `$` to `RUB`
- Improved computed data handling for empty states

**CategoryChart.vue:**
- Fixed category filtering logic (Debit transactions only)
- Updated field names: `typeName` → `type`, `size` → `debitSize`
- Improved account/category lookup with UUIDs
- Better handling of nested subcategories

### 6. Main App (`src/App.vue`)

**Changes:**
- Updated data fetching to handle paginated responses
- Changed `fetchCategory()` to `fetchCategories()` - fetches both expense and income categories
- Updated delete handlers to call actual API endpoints
- Fixed transaction type handling (removed manual conversion)

### 7. Profile View (`src/views/ProfileTab.vue`)

**Changes:**
- Migrated from Options API to Composition API
- Improved error handling for user info retrieval
- Better styling and layout

## Data Flow Examples

### Creating an Account
```javascript
// Frontend
await finApi.createAccount({
  name: 'My Account',
  balance: 1000,
  currency: 'RUB',
  accountType: 'checking'
})

// Backend expects:
{
  "name": "My Account",
  "balance": 1000,
  "currency": "RUB",
  "description": "",
  "interest_rate": null,
  "is_emergency_fund": false,
  "decimal_places": 2,
  "is_archived": false,
  "is_primary": false,
  "account_type": "checking"
}
```

### Creating a Transaction (Debit)
```javascript
// Frontend
await finApi.createTransaction({
  type: 'Debit',
  debitSize: 500,
  FROM: accountId,
  category: categoryId,
  date: '2024-01-15'
})

// Backend expects:
{
  "type": "debit",
  "debitSize": 500,
  "creditSize": null,
  "FROM": "uuid-here",
  "TO": null,
  "category": "uuid-here",
  "date": "2024-01-15",
  "description": "",
  "exchangeRate": 1,
  "splitType": null,
  "status": "settled",
  "distributions": [],
  "positions": []
}
```

### Fetching Transactions with Pagination
```javascript
// Frontend
const response = await finApi.getTransactions(0, 50)
transactions.value = response.items // Array of transaction objects

// Backend returns:
{
  "items": [...],
  "total": 150,
  "skip": 0,
  "limit": 50,
  "has_more": true
}
```

## Common Issues and Solutions

### Issue: Category Type Filtering Not Working
**Solution:** Use computed properties with proper filtering for nested subcategories
```javascript
const debitCategories = computed(() => {
  if (!props.categories) return []
  return props.categories.filter(cat => 
    cat.type === 'Debit' || 
    (Array.isArray(cat.subCategory) && 
     cat.subCategory.some(sub => sub.type === 'Debit'))
  )
})
```

### Issue: UUID Comparison in Filters
**Solution:** Always convert to string for comparison
```javascript
categories.value = categories.value.filter(
  cat => String(cat.id) !== categoryId
)
```

### Issue: Empty State Handling
**Solution:** Add defensive checks before accessing array properties
```javascript
if (!props.transactions || props.transactions.length === 0) {
  return []
}
```

## Testing Checklist

- [ ] Account creation with all fields
- [ ] Category creation (Debit and Credit types)
- [ ] Transaction creation (Debit, Adding, Transfer)
- [ ] Pagination on all list endpoints
- [ ] Delete operations for accounts, categories, transactions
- [ ] User profile display after login
- [ ] Currency formatting in charts
