---
name: isolation-test-findings
description: Data isolation QA results (task 9.2.2) — all 7 cross-user access attempts return 404 correctly; form field gotchas documented
metadata:
  type: project
---

Tested on 2026-06-16. Task 9.2.2: cross-user data isolation verification.

## Test Setup

- User A: qa_user_a@test.com / Senha@12345 (registered via /cadastro/)
- User B: qa_user_b@test.com / Senha@12345 (registered via /cadastro/)
- Resources created as User A: Account PK=4, Category PK=5, Transaction PK=7 (PKs are session-dependent and will change if DB is reset)

## Isolation Results — All PASS

All 7 access attempts by User B to User A's resources returned HTTP 404:

| Method | URL | HTTP | Result |
|--------|-----|------|--------|
| GET    | /contas/4/editar/       | 404 | PASS |
| POST   | /contas/4/toggle/       | 404 | PASS |
| GET    | /categorias/5/editar/   | 404 | PASS |
| POST   | /categorias/5/toggle/   | 404 | PASS |
| GET    | /transacoes/7/editar/   | 404 | PASS |
| GET    | /transacoes/7/excluir/  | 404 | PASS |
| POST   | /transacoes/7/excluir/  | 404 | PASS |

## Data Integrity Confirmed

After all User B access attempts, User A's data remained intact:
- Account PK=4 ("Conta Nubank QA") still present in /contas/
- Category PK=5 still present in /categorias/
- Transaction PK=7 still present in /transacoes/

## Form Field Gotchas (important for future test scripts)

- **Login form**: Django AuthenticationForm uses field name `username` (not `email`) even when USERNAME_FIELD='email'. Always POST `username=<email_value>` to /login/.
- **Category form**: field is `transaction_type` (not `category_type`). Values: 'income' or 'expense'.
- **Account form**: field is `account_type`. Values: 'checking', 'savings', 'cash', 'investment', 'credit_card'.
- **Transaction form**: fields are `description`, `amount`, `transaction_type`, `date` (YYYY-MM-DD), `account` (pk), `category` (pk), `notes`.

## How Isolation Is Enforced in Code

- `AccountUpdateView.get_queryset()` → `Account.objects.filter(user=self.request.user)` → returns 404 via get_object_or_404 when PK not in user's queryset
- `AccountToggleView.post()` → `get_object_or_404(Account, pk=pk, user=request.user)` → explicit 404
- `CategoryUpdateView.get_queryset()` → `Category.objects.filter(user=self.request.user)`
- `CategoryToggleView.post()` → `get_object_or_404(Category, pk=pk, user=request.user)`
- `TransactionUpdateView.get_queryset()` → `Transaction.objects.filter(user=self.request.user)`
- `TransactionDeleteView.get_queryset()` → `Transaction.objects.filter(user=self.request.user)`

**Why:** Django's UpdateView/DeleteView call get_object() which calls get_queryset(), so filtering queryset by user is the correct isolation pattern for CBVs.
**How to apply:** In future QA sessions, data isolation can be considered fully verified for these 6 endpoints. Only re-test if views are refactored.
