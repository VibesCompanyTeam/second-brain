---
title: "Sicurezza e dati"
type: policy
status: active
owner: responsabile-conoscenza
created: 2026-11-04
review_at: 2027-02-04
tags: [sicurezza, dati]
visibility: team
---

# Sicurezza e dati

## Cosa non scrivere nel repository

- Password, token, chiavi private e altre credenziali, nemmeno in `00-inbox/`.
- Dati personali non necessari: preferisci ruoli e riferimenti ai nomi quando bastano.
- Dati di clienti, salvo che contratti e condizioni dei fornitori usati lo consentano.
- Materiale che non tutti i membri possono leggere: i permessi valgono per l'intero repository e
  `visibility` non limita l'accesso.

## Se un segreto finisce nel repository

La cronologia Git conserva il segreto anche dopo aver cancellato il file. La scansione in CI lo segnala
solo dopo il push, quindi non lo tiene fuori da GitHub e riconosce solo i formati noti. Per controllare
prima, esegui `gitleaks git --redact .` se hai installato lo strumento.

1. Revoca o ruota subito il segreto: è il passo che elimina il rischio, e va fatto per primo.
2. Avvisa il responsabile del repository.
3. Controlla nei registri del servizio se il segreto è stato usato.
4. Se serve, riscrivi la cronologia con il responsabile, avvisando chi ha un clone. Non sostituisce
   la revoca.

## Strumenti AI

- Collegando uno strumento AI, il contenuto letto arriva al suo fornitore. Prima di collegarlo,
  verifica le condizioni del piano in uso.
- Usa un accesso individuale e in sola lettura, mai un token condiviso.
- Il contenuto dei documenti può contenere istruzioni nascoste, per esempio in testo copiato dal web.
  Controlla le azioni proposte da uno strumento AI prima di approvarle.

La procedura è in [`collegare-strumenti-ai.md`](../../04-knowledge/playbooks/collegare-strumenti-ai.md).

## Accessi

- Il repository di un'azienda reale è sempre privato e appartiene a un'organizzazione GitHub: in un
  repository personale tutti i collaboratori hanno accesso in scrittura. Ruoli, SSO e protezione dei
  branch dipendono dal piano scelto.
- Ogni collaboratore attiva l'autenticazione a due fattori. Dove il piano lo consente, va imposta
  dall'organizzazione.
- Quando qualcuno lascia il team, rimuovi subito il suo accesso e i suoi collegamenti.

## Backup

GitHub e i cloni locali non sostituiscono un backup. Prima di inserire contenuti critici va attivato un
backup cifrato fuori da GitHub, con il Recovery test previsto dalla
[policy di governance](knowledge-governance.md).
