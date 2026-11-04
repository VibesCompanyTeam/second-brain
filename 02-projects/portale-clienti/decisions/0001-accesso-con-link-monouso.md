---
title: "Accesso con link monouso"
type: decision
status: accepted
owner: delivery
created: 2026-10-02
review_at: 2027-04-02
project: portale-clienti
decision_makers: [delivery, direzione]
demo: true
visibility: team
---

# ADR-0001 del progetto: accesso con link monouso

## Contesto

I clienti pilota accedono poche volte al mese: dimenticherebbero una password dedicata.

## Decisione

Accesso con link monouso via email, valido 15 minuti.

## Opzioni considerate

- **Password:** più lavoro di assistenza.
- **Accesso con account aziendale:** non tutti i clienti pilota ne dispongono.

## Conseguenze

Chi controlla la casella email del cliente può accedere al portale. Per limitare questo rischio, nella prima versione il portale è di sola consultazione.
