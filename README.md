# Second Brain

Un sistema per conservare la conoscenza di un'azienda: cosa sappiamo, cosa abbiamo deciso, cosa stiamo
facendo e perché. È scritto in Markdown, versionato con Git e pensato per essere letto sia dalle persone sia
dagli strumenti AI che usano, come Claude Desktop e ChatGPT.

<!-- demo:start -->
> **Questa è una demo.** Contiene la conoscenza di Studio Alderano, un'azienda inventata: nomi, cifre e
> decisioni sono fittizi. **[Prova le domande della demo](DEMO.md)** o sfoglia l'[indice](INDEX.md).

## Perché non è un semplice archivio di note

- **Ogni documento dichiara quanto è affidabile.** Stato, responsabile e data di revisione distinguono una
  decisione approvata da una proposta o da un'informazione superata.
- **Le decisioni conservano il perché.** Vengono sostituite, non riscritte, e restano anche quelle respinte.
- **Gli strumenti AI ricevono regole chiare.** Citano le fonti e non scambiano una bozza per una decisione.
- **I file restano vostri.** Sono testo semplice su Git, senza dipendere da un'applicazione.

**Limite attuale:** il collegamento da Claude Desktop e ChatGPT è documentato ma non ancora provato. Il
contenuto e le regole sono stati provati con un agente AI che leggeva i file direttamente.

## Usarlo come base per un'azienda

Lo strumento rimuove la demo, riporta i documenti del sistema a `proposed` per l'approvazione interna e
rigenera l'indice:

```sh
uv run tools/new_client.py --owner responsabile-conoscenza          # mostra cosa cambierà
uv run tools/new_client.py --owner responsabile-conoscenza --apply  # applica le modifiche
```

Poi pubblica il risultato in un **nuovo repository privato**, senza la cronologia di questo, e rivedi la
[policy su sicurezza e dati](01-company/policies/sicurezza-e-dati.md).

Il codice e i documenti sono coperti da tutti i diritti riservati: per adottarlo, contatta
[VibesCompanyTeam](https://github.com/VibesCompanyTeam).
<!-- demo:end -->

## Dove trovare le risposte

| Domanda | Dove guardare |
| --- | --- |
| Cosa sappiamo? | `04-knowledge/`, `03-areas/`, `01-company/policies/` |
| Cosa abbiamo deciso? | `05-decisions/`, `02-projects/<progetto>/decisions/` |
| Cosa stiamo facendo? | `02-projects/` per il contesto, GitHub Issues per i task |
| Perché lo stiamo facendo? | `01-company/mission/`, `01-company/strategy/`, `overview.md` di ogni progetto |

## Principi

- **Le conversazioni non sono conoscenza.** Una chat può generare informazioni, ma diventano ufficiali solo
  come documento, decisione o issue verificabile.
- **Ogni documento ha un responsabile e una scadenza.** `status`, `owner` e `review_at` evitano che
  informazioni obsolete vengano riprese come se fossero valide.
- **Le decisioni non si riscrivono.** Una nuova decisione sostituisce la precedente e la indica in
  `supersedes`.
- **I task stanno in un solo posto:** GitHub Issues.
- **Prima le fonti, poi gli strumenti.** Nessuna applicazione su misura finché non sappiamo che i contenuti
  sono utili e affidabili.

## Per iniziare

Servono [Git](https://git-scm.com/) e [uv](https://docs.astral.sh/uv/). Per leggere e scrivere puoi usare un
qualsiasi editor Markdown, oppure aprire la cartella come vault in [Obsidian](https://obsidian.md/) seguendo
[questa guida](04-knowledge/playbooks/usare-obsidian.md).

```sh
uv run tools/check_docs.py
```

## Struttura

```text
00-inbox/       note grezze da classificare, non ancora conoscenza ufficiale
01-company/     missione, strategia, policy
02-projects/    una cartella per progetto: overview, requirements, architecture, decisions
03-areas/       responsabilità continue: engineering, product, sales, operations
04-knowledge/   ricerca, pattern, playbook
05-decisions/   decisioni che riguardano più progetti (ADR)
06-meetings/    verbali di riunione
07-templates/   modelli da copiare
99-archive/     materiale non più valido, ignorato salvo richiesta esplicita
tools/          verifica dei documenti, indice, preparazione di una nuova installazione
INDEX.md        elenco generato di tutti i documenti, con stato e responsabile
AGENTS.md       regole per gli strumenti AI (CLAUDE.md rimanda qui)
```

## Come contribuire

| Voglio… | Come | Modello |
| --- | --- | --- |
| Appuntare un'idea | Nota in `00-inbox/` | Nessuno |
| Scrivere conoscenza o un playbook | File in `04-knowledge/` o `03-areas/` | [`document.md`](07-templates/document.md) |
| Registrare una decisione | `05-decisions/NNNN-titolo.md` | [`decision.md`](07-templates/decision.md) |
| Avviare un progetto | `02-projects/<nome>/overview.md` | [`project-overview.md`](07-templates/project-overview.md) |
| Salvare un verbale | `06-meetings/AAAA-MM-GG-titolo.md` | [`meeting.md`](07-templates/meeting.md) |
| Assegnare un'attività | GitHub Issue | Nessuno |

### Revisione

La revisione dipende dallo stato del documento, non dalla cartella:

- **Commit diretto:** note in `00-inbox/`, documenti `draft` o `proposed` e verbali, che registrano un evento
  e non approvano nulla.
- **Pull request:** passaggio a `active` o `accepted` e qualsiasi modifica a un documento già in uno di questi
  stati.

### Metadati e verifica

Ogni documento, tranne quelli in `00-inbox/`, `07-templates/` e `99-archive/` e i file `README.md`, inizia con
un blocco di metadati. Valori ammessi, stati, procedure e routine sono nella
[policy di governance](01-company/policies/knowledge-governance.md).

```sh
uv run tools/build_index.py  # rigenera INDEX.md
uv run tools/check_docs.py   # verifica metadati, link interni e numeri di decisione
```

Gli errori bloccano la CI, le revisioni scadute generano solo un avviso.

## Strumenti AI

Le regole sono in [`AGENTS.md`](AGENTS.md): citare le fonti, distinguere informazioni confermate, ipotesi e
documenti obsoleti, non trasformare una conversazione in una decisione. Questi strumenti non le caricano
sempre da soli: la [guida](04-knowledge/playbooks/collegare-strumenti-ai.md) spiega come riportarle e come
provare l'accesso in sola lettura.

## Controlli

| Controllo | Come funziona |
| --- | --- |
| Metadati, link interni, numeri di decisione | Verificati in CI |
| Indice | Generato e controllato in CI |
| Segreti | gitleaks in CI su tutta la cronologia, dopo il push |
| Azioni CI | Bloccate per SHA e aggiornate da Dependabot |
| Backup e accesso degli strumenti AI | Da configurare su ogni installazione |

Le regole di sicurezza sono in [`sicurezza-e-dati.md`](01-company/policies/sicurezza-e-dati.md).
