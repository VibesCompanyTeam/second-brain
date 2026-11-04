---
title: "Governance della conoscenza"
type: policy
status: active
owner: responsabile-conoscenza
created: 2026-11-04
review_at: 2027-02-04
tags: [governance]
visibility: team
---

# Governance della conoscenza

## Metadati

Ogni documento in `01-company/` … `06-meetings/` inizia con questo blocco. `00-inbox/`,
`07-templates/`, `99-archive/` e i file `README.md` sono esclusi dalla verifica.

| Campo | Obbligatorio | Valori |
| --- | --- | --- |
| `title` | sì | testo |
| `type` | sì | `policy`, `strategy`, `project`, `requirement`, `architecture`, `decision`, `knowledge`, `playbook`, `research`, `meeting` |
| `status` | sì | vedi sotto |
| `owner` | sì | persona o team responsabile |
| `created` | sì | `AAAA-MM-GG` |
| `review_at` | sì, tranne `meeting` | `AAAA-MM-GG`, non precedente a `created` |
| `visibility` | sì | `team`, `project` |
| `project`, `tags` | no | testo, elenco |
| `sources` | no | elenco di percorsi o link da cui deriva il contenuto |
| `decision_makers` | no | elenco di chi ha deciso, per le decisioni |
| `supersedes` | no | percorso del documento sostituito |

## Stati

| Stato | Significato | Come trattarlo |
| --- | --- | --- |
| `draft` | in lavorazione | ipotesi |
| `proposed` | pronto per la revisione, non approvato | ipotesi |
| `active` | valido e in uso | confermato |
| `accepted` | decisione approvata | confermato |
| `rejected` | decisione scartata | da non applicare, utile come contesto |
| `deprecated` | non più valido, senza sostituto | obsoleto |
| `superseded` | sostituito da un altro documento | obsoleto |

## Revisione

| Modifica | Come |
| --- | --- |
| Note in `00-inbox/`, documenti `draft` o `proposed`, verbali | Commit diretto |
| Passaggio a `active` o `accepted` | Pull request |
| Qualsiasi modifica a un documento `active` o `accepted` | Pull request |

Fanno eccezione i verbali, che pur avendo stato `active` registrano un evento e non approvano nulla.
Le decisioni emerse in riunione diventano ADR. La regola non è imposta da protezioni del branch.

## Procedure

- **Sostituire una decisione:** crea un nuovo ADR con `supersedes` e, nella stessa pull request, porta
  quello vecchio a `superseded` aggiungendo in testa un link al nuovo. Il resto del testo non cambia.
- **Gestire una revisione scaduta:** il responsabile conferma il documento e sposta `review_at`,
  oppure lo aggiorna, oppure lo porta a `deprecated`.
- **Archiviare:** sposta in `99-archive/` i documenti `deprecated`, `superseded` o `rejected` che non
  servono più come contesto, mantenendo i metadati. Le decisioni restano in `05-decisions/`, così la
  loro numerazione e i riferimenti rimangono validi.
- **Cambiare responsabile:** quando una persona lascia il team o cambia ruolo, aggiorna `owner` dei
  suoi documenti con una pull request. Chi subentra verifica anche `review_at`.

## Livelli di memoria

| Livello | Contenuto | Dove | Aggiornamento |
| --- | --- | --- | --- |
| Working | conversazioni e attività correnti | fuori dal repository, `00-inbox/` | automatico, temporaneo |
| Episodic | riunioni, eventi, decisioni, risultati | `06-meetings/`, `05-decisions/` | estrazione con revisione |
| Semantic | conoscenza consolidata, procedure, architetture | `01-company/` … `04-knowledge/` | versionato e approvato |

## Routine

| Routine | Frequenza | Attività |
| --- | --- | --- |
| Inbox triage | ogni giorno | classificare nuove note e richieste |
| Decision capture | dopo ogni decisione | registrare cosa è stato deciso e perché |
| Weekly review | ogni venerdì | aggiornare progetti, blocchi e priorità |
| Knowledge audit | ogni mese | gestire le revisioni scadute, elencate da `uv run tools/check_docs.py`, e cercare a mano i duplicati |
| Recovery test | ogni trimestre | verificare backup e ripristino |
