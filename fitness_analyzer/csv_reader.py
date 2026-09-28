"""
7. **Lag lesing av `participants.csv`.** Fil: `fitness_analyzer/csv_reader.py`. 
Bruk `with open(..., encoding="utf-8", newline="")` og Pythons `csv`module, akkurat som oppgaven sier. 
Hver rad skal konverteres fra strings til riktige typer, for eksempel `int`/`float`, valideres og bli 
et `Participant`objekt. Det er praktisk å lagre participants i en dictionary etter ID, 
omtrent `{ "P001": participant_object }`. Forelesning: `class1.py` for dictionaries, `class2.py` for loops. 
**Ingen av forelesningene du har lastet opp går ordentlig gjennom `csv`modulen**, så her er det selve Assignment II som er hovedkilden.

8. **Lag lesing av session-CSV.** Fil: `fitness_analyzer/csv_reader.py`. 
Les `fitness_sessions.csv` og sørg også for at programmet kan behandle `fitness_sessions_invalid.csv`. 
Konverter `timestamp`, `heart_rate`, `skin_response`, `temperature`, `activity_level` og `signal_quality` 
til riktige datatyper. 
Forelesning: samme som punkt 7 pluss **Error Handling in Python** for konverteringsfeil.

9. **Valider hver CSV-rad og fortsett når én rad er dårlig.** Fil: `fitness_analyzer/csv_reader.py` sammen med `validation.py` og `exceptions.py`. 
Her skal du oppdage manglende felt, feil datatype, ugyldig ID, ukjent participant, umulige målinger og dårlig signal. 
En dårlig rad skal ikke nødvendigvis krasje hele programmet; den registreres som rejected og programmet 
går videre. Forelesning: **Error Handling in Python**, særlig focused handlers. 
Forelesningen anbefaler konkrete `except ValueError:` osv. fremfor brede `except:`. Oppgaven sier det samme.

10. **Registrer informasjon om alle rejected rows.**  Fil: sannsynligvis `fitness_analyzer/csv_reader.py`. 
For hver rejected rad trenger vi å lagre minst `source filename`, `row number`, `field` og `reason`. 
Dette kan først være dictionaries i en liste. Eksempelidé: `{"filename": ..., "row": ..., "field": ..., 
"reason": ...}`. Forelesning: `class1.py` for dictionaries/lists og `class2.py` for loops. Dette er et direkte Assignment II-krav.

11. **Gruppér observations etter `session_id`.** Fil: `fitness_analyzer/csv_reader.py`. 
Flere CSV-rader tilhører samme fitness-session. 
De må samles slik at vi ender med ett `Session`objekt med mange `Observation`objekter. 
Sessionen skal også kobles til riktig eksisterende `Participant`. 
Forelesning: `class1.py` for dictionaries/lists og OOP-forelesningene for composition. 
Assignment II krever eksplisitt grouping og kobling til eksisterende participant.

"""
"""
**Lag lesing av session-CSV.** Fil: `fitness_analyzer/csv_reader.py`. 
Les `fitness_sessions.csv` og sørg også for at programmet kan behandle `fitness_sessions_invalid.csv`. 
Konverter `timestamp`, `heart_rate`, `skin_response`, `temperature`, `activity_level` og `signal_quality` 
til riktige datatyper. 
Forelesning: samme som punkt 7 pluss **Error Handling in Python** for konverteringsfeil.

"""

import csv

from fitness_analyzer.models import Participant, Observation, Session
from fitness_analyzer.validation import validate_participant, validate_participant_id

def load_participants(filename):
    participants = {}

    with open(filename, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            participant_id = row["participant_id"]
            name = row["name"]

            baseline_heart_rate = int(row["baseline_heart_rate"])
            baseline_skin_response = float(row["baseline_skin_response"])
            baseline_temperature = float(row["baseline_temperature"])

            validate_participant_id(participant_id)

            participant = Participant(
                participant_id,
                name,
                baseline_heart_rate,
                baseline_skin_response,
                baseline_temperature
            )

            participants[participant_id] = participant

    return participants





    

    

