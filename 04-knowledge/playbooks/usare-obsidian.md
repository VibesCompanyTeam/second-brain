---
title: "Usare Obsidian con il repository"
type: playbook
status: active
owner: responsabile-conoscenza
created: 2026-11-04
review_at: 2027-02-04
sources:
  - 05-decisions/0001-git-markdown-come-fonte-di-verita.md
tags: [obsidian, git]
visibility: team
---

# Usare Obsidian con il repository

Obsidian è facoltativo: legge e modifica i file del tuo clone locale. La versione di riferimento resta
quella su GitHub.

## Prima configurazione

1. Clona il repository come indicato nel [README](../../README.md).
2. In Obsidian scegli **Apri cartella come vault** e seleziona il clone.

Il repository include `.obsidian/app.json`, che imposta link Markdown standard, percorsi relativi e
aggiornamento dei link quando sposti un file. Così i link restano validi anche su GitHub e negli
strumenti AI: non cambiare queste impostazioni.

## Lavoro quotidiano

1. Prima di iniziare, aggiorna il clone con `git pull`.
2. Per un nuovo documento, copia un modello da `07-templates/` nella cartella giusta.
3. Prima del push, esegui `uv run tools/build_index.py` e `uv run tools/check_docs.py`.
4. Segui le [regole di revisione](../../README.md#revisione): commit diretto o pull request a seconda
   dello stato del documento.

## Sincronizzazione

Usa un solo meccanismo: Git. Non attivare Obsidian Sync, iCloud, Dropbox o simili sulla stessa cartella,
perché competerebbero sugli stessi file. Se scrivere da mobile diventa necessario, va rivalutato come
indicato in [ADR-0001](../../05-decisions/0001-git-markdown-come-fonte-di-verita.md).
