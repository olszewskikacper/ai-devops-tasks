# Pipeline CI/CD w Jenkinsie dla aplikacji webowej

```mermaid
flowchart TD
    A[Checkout kodu] --> B[Budowanie]
    B --> C[Testy jednostkowe]
    C --> D[Analiza statyczna kodu]
    D --> E[Skanowanie bezpieczeństwa]
    E --> F[Budowanie obrazu Docker]
    F --> G[Testy integracyjne]
    G --> H[Wdrożenie na staging]
    H --> I{Zatwierdzenie ręczne}
    I -->|Zatwierdzone| J[Wdrożenie na produkcję]
    I -->|Odrzucone| K[Koniec bez wdrożenia]

    B & C & D & E & F & G & H & J -->|błąd| X[Powiadomienie o błędzie]
```
