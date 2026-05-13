# Frontend Changes Summary

## Quick Reference for API Integration

### Field Name Mappings

| Old Frontend Field | New Backend Field | Notes |
|-------------------|-------------------|-------|
| `typeName` | `type` | 'Debit', 'Adding', or 'Transfer' |
| `size` | `debitSize` | For adding: `creditSize` is used |
| `exchange_rate` | `exchangeRate` | CamelCase now |
| `category` (as number) | `category` (as UUID string) | Always use UUIDs |

### Category Type Mappings

| Frontend Display | Backend API Value |
|-----------------|-------------------|
| Expense | Debit |
| Income | Credit |

## Key Updates Made

### 1. API Layer (`src/api/finApi.js`)
- ✅ Added pagination support to all GET endpoints
- ✅ Added separate methods for expense/income categories
- ✅ Added account CRUD operations
- ✅ Fixed field name mappings (camelCase)
- ✅ Added error handling with proper logging

### 2. Components Updated

#### TopAccounts.vue
- Simplified account creation payload
- Removed hardcoded currency logic

#### TopCategories.vue  
- Fixed category filtering for nested structures
- Changed delete handler signature
- Added computed properties for reactive filtering

#### TransactionTable.vue
- Updated all field references to match backend
- Fixed category lookup functions
- Improved modal form handling

#### CategoryChart.vue
- Fixed transaction type filtering (Debit only)
- Updated field names throughout
- Better empty state handling

#### PortfolioChart.vue
- Changed currency from `$` to `RUB`
- Improved computed data structure

### 3. Views Updated

#### ProfileTab.vue
- Migrated to Composition API (`<script setup>`)
- Better error handling for user info retrieval

#### App.vue
- Updated data fetching to handle paginated responses
- Changed `fetchCategory()` → `fetchCategories()`
- Integrated real API calls for delete operations

## Usage Examples

### Create Account
```javascript
await finApi.createAccount({
  name: 'Savings',
  balance: 5000,
  currency: 'RUB',
  accountType: 'savings'
})
```

### Create Transaction (Debit)
```javascript
await finApi.createTransaction({
  type: 'Debit',
  debitSize: 1000,
  FROM: accountId,
  category: categoryId,
  date: '2024-05-13'
})
```

### Fetch with Pagination
```javascript
const response = await finApi.getTransactions(0, 50)
// response.items contains the transactions array
```

## Testing Commands

```bash
# Build for production
npm run build

# Development server
npm run dev

# Lint check
npm run lint
```

## Known Limitations

1. **Distributions & Positions**: Not yet fully implemented in UI
2. **Transaction Status**: Defaulting to 'settled' - pending/partially_paid not exposed in forms yet
3. **Category Hierarchy**: Subcategory display needs improvement for deeply nested structures

## Next Steps

- [ ] Add transaction editing functionality
- [ ] Implement distribution settlement UI
- [ ] Add position tracking interface
- [ ] Improve category hierarchy visualization
- [ ] Add date range filters for transactions
- [ ] Implement export functionality
