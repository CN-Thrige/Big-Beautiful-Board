# Modfase – Eksempler med Random

## Hvad er modfase?

**Modfase** betyder, at to ting altid er hinandens modsætning. Når den ene lysdiode er tændt, er den anden slukket – og omvendt. De er aldrig tændt samtidig, og aldrig slukket samtidig.

| LED1 (p1) | LED2 (p0) |
|-----------|-----------|
| Tændt | Slukket |
| Slukket | Tændt |

**Modfase vs. "i takt":**
- **I takt** (synkront) → begge LED'er gør det *samme* på samme tid.
- **Modfase** (modsat) → de gør *hinandens modsætning* på samme tid.

---

## 1. Modfase med tilfældig blink-hastighed

```python
from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    ventetid = random.uniform(0.2, 1.0)  # tilfældig tid mellem 0.2 og 1.0 sek

    p1.on()
    p0.off()
    sleep(ventetid)

    p1.off()
    p0.on()
    sleep(ventetid)
```

**Forklaring:** Der genereres ét nyt tilfældigt tal *per runde*, som bruges til begge `sleep()`-kald. Modfasen er 100% intakt — LED'erne er stadig altid hinandens modsætning — men hastigheden varierer fra runde til runde.

**Brug til eksamen:** Det mest "sikre" eksempel at bygge videre på. Stadig tydelig modfase, men viser du kan integrere `random`-biblioteket. God til opgaver der beder om at gøre blink-mønsteret mere dynamisk oveni modfase-kravet.

---

## 2. Hver diode har sin egen tilfældige hastighed

```python
from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

while True:
    t1 = random.uniform(0.1, 0.8)
    t2 = random.uniform(0.1, 0.8)

    p1.on()
    p0.off()
    sleep(t1)

    p1.off()
    p0.on()
    sleep(t2)
```

**Forklaring:** To *forskellige* tilfældige tal genereres — ét for hvor længe p1 er tændt (p0 slukket), og ét for hvor længe p0 er tændt (p1 slukket). Selvom tiderne er forskellige, er det stadig modfase, fordi der aldrig er et tidspunkt hvor begge er tændt eller begge er slukket samtidig.

**Brug til eksamen:** Nyttig hvis opgaven spørger, hvordan man kan gøre programmet mere uforudsigeligt uden at bryde modfase-kravet. Viser forståelse af *hvad* modfase egentlig kræver (aldrig samme tilstand samtidig).

---

## 3. Tilfældigt valg af hvilken diode der starter

```python
from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

while True:
    if random.choice([True, False]):
        p1.on(); p0.off()
    else:
        p1.off(); p0.on()

    sleep(0.5)
```

**Forklaring:** I hver runde vælges tilfældigt (50/50), om p1 eller p0 skal være den tændte. Men *inden for* samme runde er de stadig garanteret modsatte af hinanden.

**Brug til eksamen:** Godt eksempel til at demonstrere `random.choice()` og til at vise, at modfase-relationen (`if/else` med modsatte værdier) kan kombineres med tilfældighed i *hvilken* gren der vælges, uden at bryde selve definitionen.

---

## 4. Random + knap: modfase vs. "flimmer"

```python
from machine import Pin
from time import sleep
import random

button1 = Pin(6, Pin.IN, Pin.PULL_UP)
p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

def modfase():
    p1.on(); p0.off()
    sleep(0.5)
    p1.off(); p0.on()
    sleep(0.5)

def random_flimmer():
    p1.value(random.randint(0, 1))
    p0.value(random.randint(0, 1))
    sleep(random.uniform(0.05, 0.3))

while True:
    if button1.value() == 0:
        random_flimmer()
    else:
        modfase()
```

**Forklaring:** Bygger videre på den klassiske eksamensstruktur (knap styrer to tilstande). I stedet for "i takt" bruges her en tilstand, hvor begge LED'er sættes **helt uafhængigt** af hinanden via `random.randint(0, 1)` — de kan altså begge være tændt, begge slukket, eller modsatte, helt tilfældigt.

**Vigtigt:** Dette er bevidst *ikke* modfase i flimmer-tilstanden — det skaber en kontrast, så man tydeligt kan se forskellen mellem "styret modsætning" (modfase) og "ukontrolleret tilfældighed".

**Brug til eksamen:** Kun relevant hvis opgaven beder om noget ekstra ud over de to krævede tilstande (i takt/modfase), fx en bonusdel som "tilføj en tredje tilstand". Brug det **ikke** som erstatning for "i takt", da det ikke opfylder det oprindelige krav.

---

## 5. Random antal blink i modfase, før pause

```python
from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

while True:
    antal_blink = random.randint(2, 6)

    for _ in range(antal_blink):
        p1.on(); p0.off()
        sleep(0.3)
        p1.off(); p0.on()
        sleep(0.3)

    p1.off()
    p0.off()
    sleep(random.uniform(1, 3))  # tilfældig pause mellem "serier"
```

**Forklaring:** Der køres et tilfældigt antal modfase-blink (2–6 gange) i træk, hvorefter begge LED'er slukkes, og der holdes en tilfældig pause, før mønsteret starter forfra.

**Brug til eksamen:** Viser du kan bruge en `for`-løkke sammen med `random.randint()` til at styre *gentagelser*, ikke kun værdier. God til opgaver der beder om et mønster, der ikke bare kører uendeligt ens, fx "tilføj en pause mellem blink-sekvenser".

---

## 6. Simuleret "defekt" modfase (chance for at springe skift over)

```python
from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

state = 0

while True:
    if random.random() > 0.1:  # 90% chance for normalt skift
        state = not state

    p1.value(state)
    p0.value(not state)
    sleep(0.5)
```

**Forklaring:** Der er 90% chance for, at tilstanden (`state`) skifter som normalt hver runde — men 10% af tiden springes skiftet over, så samme LED forbliver tændt lidt længere end forventet. Modfase-relationen mellem p1 og p0 er dog altid bevaret (`p0.value(not state)` sikrer det); det er kun *timingen* af skiftet, der er uforudsigelig.

**Brug til eksamen:** Det mest avancerede eksempel — kræver, at du kan forklare `random.random()` (returnerer 0.0–1.0) og hvordan en sandsynlighedstærskel fungerer. Sjældent krævet i en almindelig eksamensopgave, medmindre det er en bonusdel.

---

## Nyttige random-funktioner i MicroPython

| Funktion | Beskrivelse |
|---|---|
| `random.random()` | Flydende tal mellem 0.0 og 1.0 |
| `random.uniform(a, b)` | Flydende tal mellem a og b |
| `random.randint(a, b)` | Heltal mellem a og b (begge inklusive) |
| `random.choice(liste)` | Vælger tilfældigt element fra en liste |

Husk `import random` øverst i filen — modulet er indbygget i MicroPython, men skal importeres eksplicit.

---

## Opsummering: Hvilket eksempel skal jeg bruge?

| Eksempel | Sværhedsgrad | Bevarer modfase strikt? | Bedst til |
|---|---|---|---|
| 1 | Let | Ja | Standard-udvidelse af opgaven |
| 2 | Let–middel | Ja | At vise dybere forståelse af modfase |
| 3 | Let | Ja | Alternativ måde at variere på |
| 4 | Middel | Nej (i flimmer-delen) | Bonusopgave / kontrast-demonstration |
| 5 | Middel | Ja | Mere komplekst mønster m. løkker |
| 6 | Svær | Ja (i selve outputtet) | Avanceret bonus, sjældent krævet |

**Anbefaling:** Til en klassisk eksamensopgave om modfase (fx 10–15 point) er **eksempel 1 eller 2** det bedste valg. De holder sig strengt til modfase-definitionen, men tilføjer kompleksitet på en måde, der viser forståelse af konceptet — uden at risikere at bryde selve modfase-kravet.
