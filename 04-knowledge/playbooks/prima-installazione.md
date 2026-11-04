---
title: "Prima installazione"
type: playbook
status: active
owner: responsabile-conoscenza
created: 2026-11-04
review_at: 2027-02-04
sources:
  - 05-decisions/0001-git-markdown-come-fonte-di-verita.md
  - 01-company/policies/sicurezza-e-dati.md
tags: [installazione]
visibility: team
---

# Prima installazione

I passi per far partire il Second Brain di un'azienda, una volta rimossi i contenuti dimostrativi. I
documenti del sistema partono da `proposed`: diventano validi solo quando l'azienda li approva.

## 1. Crea il repository privato

Parti senza la cronologia del repository di origine:

```sh
rm -rf .git
git init -b main
git add -A
git commit -m "Avvia Second Brain"
gh repo create <organizzazione>/<nome> --private --source . --push
```

Controlla che la CI sia verde nella scheda **Actions**.

## 2. Configura GitHub

- Dai accesso alle persone con il ruolo minimo necessario.
- Attiva l'autenticazione a due fattori, imponendola dove il piano lo consente.
- Se il piano lo consente, attiva protezione del branch `main` e scansione dei segreti. La protezione non
  deve bloccare i commit diretti previsti dalle [regole di revisione](../../README.md#revisione).

## 3. Approva le regole

Con una pull request, rivedi questi documenti, assegna i responsabili in `owner` e portali ad `accepted` o
`active`:

- [ADR-0001](../../05-decisions/0001-git-markdown-come-fonte-di-verita.md)
- [Governance della conoscenza](../../01-company/policies/knowledge-governance.md)
- [Sicurezza e dati](../../01-company/policies/sicurezza-e-dati.md)
- [Usare Obsidian](usare-obsidian.md), se lo adottate

## 4. Inserisci i primi contenuti

Parti da pochi documenti: missione, strategia e un progetto in corso. Elimina le cartelle di area che non
servono e rigenera l'indice con `uv run tools/build_index.py`.

## 5. Attiva backup e strumenti AI

- Attiva il backup previsto dalla [policy su sicurezza e dati](../../01-company/policies/sicurezza-e-dati.md)
  prima di inserire contenuti critici.
- Collega gli strumenti AI seguendo la [guida](collegare-strumenti-ai.md), partendo da contenuti non sensibili.
