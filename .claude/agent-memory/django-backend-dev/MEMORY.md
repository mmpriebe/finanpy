# Memory Index — Django Backend Dev (Finanpy)

- [Sprint 1 — CustomUser Implementation](project_sprint1_customuser.md) — CustomUser/Manager/Admin/Forms/Views/URLs built; DB reset required; key decisions on AbstractUser vs AbstractBaseUser
- [Profiles App](project_profiles_app.md) — UserProfile signal/forms/views/URLs; no namespace on urls.py; ProfilesConfig in INSTALLED_APPS; dual-form UpdateView pattern
- [Sprint 5 — Accounts App](project_sprint5_accounts.md) — Account model/admin/form/views/URLs done; toggle uses base View; mounted at contas/; 0 system-check issues
- [Sprint 6 — Categories App](project_sprint6_categories.md) — Category model/admin/form/views/URLs done; unique_together (user,name,type); mounted at categorias/; 0 system-check issues
- [Sprint 7 — Transactions App](project_sprint7_transactions.md) — Transaction model/admin/form/views/URLs done; FKs to Account+Category with PROTECT; mounted at transacoes/; 0 system-check issues
