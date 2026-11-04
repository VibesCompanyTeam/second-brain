---
title: "Git e Markdown come fonte di verità"
type: decision
status: accepted
owner: responsabile-conoscenza
created: 2025-10-20
review_at: 2027-02-04
decision_makers: [direzione]
tags: [architettura, governance]
visibility: team
---

# ADR-0001: Git e Markdown come fonte di verità

## Contesto

L'azienda ha bisogno di un sistema di conoscenza condiviso, usato dalle persone direttamente o tramite
strumenti AI come Claude Desktop e ChatGPT. Deve mantenere autore, cronologia e stato di ogni documento
ed evitare che informazioni obsolete vengano riprese come se fossero valide.

## Decisione

- La conoscenza vive in file Markdown con metadati, in un repository Git privato.
- I task vivono solo in GitHub Issues.
- Le decisioni si registrano come ADR.
- Nessuna applicazione su misura all'inizio: la ricerca AI arriva dopo aver verificato qualità e utilità
  delle fonti.
- Obsidian è un editor locale facoltativo. Obsidian Sync si valuta, limitato a `00-inbox/`, solo se
  qualcuno non usa Git o deve scrivere spesso da mobile.

## Opzioni considerate

- **Notion**: più adatto a team non tecnici, ma meno portabile e meno diretto da usare per gli strumenti AI.
- **Outline**: wiki centralizzata da ospitare e mantenere; da rivalutare se Git diventa un ostacolo.

## Accesso dagli strumenti AI

L'interfaccia comune è un server MCP remoto: ChatGPT si collega a server remoti e i connettori
personalizzati di Claude partono dal cloud di Anthropic.

- **Primo passo:** provare il server MCP remoto ufficiale di GitHub in sola lettura, senza scrivere codice.
- **Passo successivo, solo se la prova non basta:** un piccolo server con `search` e `fetch` sul repository,
  che restituisca percorso e stato di ogni documento ed escluda `99-archive/`.
- **Scrittura:** solo proposte tramite pull request, con l'identità di chi le richiede.
- **Requisiti di accesso:** sola lettura come impostazione iniziale e un token individuale limitato al
  repository, mai un token condiviso. I limiti vanno imposti sul server, non nelle istruzioni al modello.

## Conferma

- La CI verifica documenti, indice e segreti a ogni push.
- La [guida agli strumenti AI](../04-knowledge/playbooks/collegare-strumenti-ai.md) contiene la prova di
  accesso da eseguire su ogni installazione.

## Conseguenze

- Chi scrive deve usare Git, direttamente o tramite Obsidian.
- I permessi valgono per l'intero repository: `visibility` è informativo e il materiale riservato richiede
  un repository separato.
- Ruoli distinti, SSO e protezione dei branch dipendono dal piano GitHub dell'organizzazione.
