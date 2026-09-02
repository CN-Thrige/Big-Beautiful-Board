# Modfase i MicroPython – Komplet Eksamensguide

Denne guide gennemgår **alle** dine modfase-eksempler, forklarer hvad koden gør, hvorfor den virker, og hvordan du kan bygge videre på den til en eksamensopgave.

---

## 1. Hvad er modfase? (Grundbegreb)

**Modfase** betyder, at to ting altid er hinandens modsætning:
- Når LED1 er tændt → LED2 er slukket
- Når LED1 er slukket → LED2 er tændt
- De er **aldrig** tændt samtidig, og **aldrig** slukket samtidig (medmindre man bevidst bryder mønsteret, se eksempel 4).

| LED1 (p1) | LED2 (p0) |
|-----------|-----------|
| Tændt     | Slukket   |
| Slukket   | Tændt     |

**Modfase vs. "i takt" (synkront):**
- **I takt** → begge LED'er gør *det samme* på samme tid.
- **Modfase** → de gør *hinandens modsætning* på samme tid.

Alle eksempler herunder styrer to output-pins (`p1` = rød, `p0` = gul), og forskellen ligger i **hvordan** skiftet mellem dem sker.

---

## 2. Grundlæggende (ikke-random) eksempler

Disse fire filer viser de klassiske måder at implementere modfase på **uden** tilfældighed. De er gode at kunne udenad, fordi de danner basis for alle random-varianterne.

### 2.1 `modfase_med_2_leder.py` — Den klassiske if/else-stil

```python
from machine import Pin
from time import sleep

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    p1.on()
    p0.off()
    sleep(0.5)

    p1.off()
    p0.on()
    sleep(0.5)
```

**Forklaring:** Simplest mulige modfase. To pins skiftes manuelt `on()`/`off()` med fast 0.5 sek. mellemrum.
**Sværhedsgrad:** Meget let. Dette er "skabelonen" alle andre eksempler bygger videre på.

### 2.2 `modfase_value_func.py` — Med en `state`-variabel

```python
from machine import Pin
from time import sleep

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

state = 0  # 0 eller 1

while True:
    p1.value(state)
    p0.value(not state)   # altid det modsatte af p1
    state = not state
    sleep(0.5)
```

**Forklaring:** I stedet for `on()`/`off()` bruges `.value(state)`. `p0` sættes altid til `not state`, så modfasen er *garanteret* matematisk — den kan aldrig komme ud af sync, fordi den er defineret som modsætningen af `p1`, ikke som en separat kommando.
**Fordel ift. 2.1:** Mere "elegant" kode og mindre fejlmulighed (man kan ikke ved en fejl glemme at slukke den ene). Godt at nævne til eksamen som en **forbedring**.

### 2.3 `modfase_list.py` — Med en liste af pins

```python
from machine import Pin
from time import sleep

leds = [Pin(0, Pin.OUT), Pin(1, Pin.OUT)]

state = True

while True:
    leds[0].value(state)
    leds[1].value(not state)
    state = not state
    sleep(0.5)
```

**Forklaring:** Samme logik som 2.2, men pins er samlet i en `list`. Gør koden mere skalerbar — nemt at udvide til flere LED'er ved at indeksere i listen.
**Brug til eksamen:** Godt hvis opgaven beder om en løsning, der er let at udvide, eller hvis du skal vise du forstår lister/collections i MicroPython.

### 2.4 `modfase_mellem_2_grupper_af_leder.py` — Modfase mellem *grupper*

```python
from machine import Pin
from time import sleep

gruppe_a = [Pin(0, Pin.OUT), Pin(2, Pin.OUT)]
gruppe_b = [Pin(1, Pin.OUT), Pin(3, Pin.OUT)]

while True:
    for led in gruppe_a:
        led.on()
    for led in gruppe_b:
        led.off()
    sleep(0.5)

    for led in gruppe_a:
        led.off()
    for led in gruppe_b:
        led.on()
    sleep(0.5)
```

**Forklaring:** I stedet for 2 enkelte dioder er der to **grupper** af dioder (fx 2+2 = 4 LED'er). Hele gruppe A tændes, mens hele gruppe B slukkes — og omvendt. Bruger `for`-løkker til at styre flere pins ad gangen.
**Brug til eksamen:** Perfekt hvis opgaven kræver mere end 2 LED'er, eller beder om at "udvide kredsløbet med flere dioder i samme mønster".

### 2.5 `modfase_pwm.py` — Modfase med *analog* lysstyrke (PWM)

```python
from machine import Pin, PWM
from time import sleep

pwm1 = PWM(Pin(0))
pwm0 = PWM(Pin(1))
pwm1.freq(1000)
pwm0.freq(1000)

duty = 0
retning = 1

while True:
    pwm1.duty_u16(duty)
    pwm0.duty_u16(65535 - duty)   # modsat lysstyrke af pwm1
    duty += retning * 2000

    if duty >= 65535 or duty <= 0:
        retning *= -1

    sleep(0.01)
```

**Forklaring:** Dette er en helt anderledes tilgang — i stedet for on/off bruges **PWM** (Pulse Width Modulation) til at style lysstyrken *gradvist*. `duty` går op og ned mellem 0 og 65535 (fuld skala), og den anden diode får altid den **omvendte** lysstyrke (`65535 - duty`). Resultatet: når den ene diode fader op, fader den anden ned — en "blød" version af modfase.
**Vigtigt:** Dette kræver, at din mikrocontroller/pins understøtter PWM (fx ESP32, Raspberry Pi Pico). Tjek det, før du bruger det til eksamen.
**Brug til eksamen:** Avanceret bonusopgave — viser du forstår PWM og kan tænke modfase-konceptet ud over simpelt on/off. Kun relevant hvis opgaven specifikt nævner lysstyrke/dæmpning eller PWM.

---

## 3. Random-baserede eksempler

Disse seks eksempler tager grundmønsteret og tilføjer `random`-modulet på forskellige måder. **Fælles pointe:** Modfase handler om *relationen* mellem de to dioder (de må aldrig have samme tilstand samtidig) — ikke om *timingen*. Derfor kan man tilføje masser af tilfældighed uden at bryde modfasen, så længe man passer på relationen.

### 3.1 `Modfase med tilfældig blink-hastighed.py`

```python
ventetid = random.uniform(0.2, 1.0)
p1.on(); p0.off(); sleep(ventetid)
p1.off(); p0.on(); sleep(ventetid)
```

**Forklaring:** Ét nyt tilfældigt tal genereres *per runde* og bruges til **begge** `sleep()`-kald. Modfasen er 100 % intakt, men hastigheden varierer runde for runde.
**Sværhedsgrad:** Let. Det sikreste og mest anbefalede eksempel at bygge videre på til en almindelig eksamensopgave.

### 3.2 `Hver diode har sin egen tilfældige hastighed.py`

```python
t1 = random.uniform(0.1, 0.8)
t2 = random.uniform(0.1, 0.8)
p1.on(); p0.off(); sleep(t1)
p1.off(); p0.on(); sleep(t2)
```

**Forklaring:** To *forskellige* tilfældige tal — ét for hvor længe p1 er tændt, ét for hvor længe p0 er tændt. Stadig modfase, fordi der aldrig er et tidspunkt hvor begge er tændt/slukket samtidig — kun *varigheden* af hver tilstand varierer.
**Brug til eksamen:** Viser du forstår *hvad* modfase egentlig kræver (aldrig samme tilstand samtidig), fremfor bare at kopiere et mønster.

### 3.3 `Tilfældigt valg af hvilken diode der starter.py` (findes i 2 identiske kopier)

```python
if random.choice([True, False]):
    p1.on(); p0.off()
else:
    p1.off(); p0.on()
sleep(0.5)
```

**Forklaring:** Hver runde vælges 50/50 tilfældigt, om p1 eller p0 skal være den tændte — men *inden for* samme runde er de garanteret modsatte.
**Bemærk:** Du har **to identiske filer** med dette indhold (`(1).py`-versionen er en dublet). Du kan roligt slette den ene, de gør præcis det samme.
**Brug til eksamen:** Godt eksempel på `random.choice()` kombineret med modfase-logik.

### 3.4 `Random + knap_ modfase når sluppet, tilfældigt flimmer når trykket.py`

```python
def modfase():
    p1.on(); p0.off(); sleep(0.5)
    p1.off(); p0.on(); sleep(0.5)

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

**Forklaring:** Bygger videre på den klassiske eksamensstruktur (knap styrer to tilstande). I "flimmer"-tilstanden sættes begge LED'er **helt uafhængigt** med `random.randint(0, 1)` — de kan altså begge være tændt, begge slukket, eller modsatte, helt tilfældigt.
**⚠️ Vigtigt:** Dette er **bevidst IKKE modfase** i flimmer-delen. Det bruges til at skabe en **kontrast**, så man tydeligt kan vise forskellen mellem "styret modsætning" (modfase) og "ukontrolleret tilfældighed" (flimmer).
**Brug til eksamen:** Kun relevant som en **bonusdel** (fx "tilføj en tredje tilstand"). Brug den **ikke** som erstatning for den klassiske "i takt"-tilstand, hvis opgaven kræver den — for den opfylder ikke det krav.

### 3.5 `Random antal blink i modfase, før pause.py`

```python
while True:
    antal_blink = random.randint(2, 6)
    for _ in range(antal_blink):
        p1.on(); p0.off(); sleep(0.3)
        p1.off(); p0.on(); sleep(0.3)
    p1.off(); p0.off()
    sleep(random.uniform(1, 3))
```

**Forklaring:** Kører et tilfældigt antal modfase-blink (2–6) i træk, slukker derefter begge LED'er, og holder en tilfældig pause, før mønsteret starter forfra.
**Brug til eksamen:** Viser du kan kombinere en `for`-løkke med `random.randint()` til at styre *gentagelser* (ikke bare enkeltværdier). God til opgaver, der beder om et mønster med "serier" og pauser.

### 3.6 `Simulerer defekt modfase – tilfældig chance for at springe et skift over.py`

```python
state = 0
while True:
    if random.random() > 0.1:  # 90% chance for normalt skift
        state = not state
    p1.value(state)
    p0.value(not state)
    sleep(0.5)
```

**Forklaring:** 90 % chance for, at `state` skifter som normalt — men 10 % af tiden springes skiftet over, så samme LED forbliver tændt lidt længere. Modfasen (`p0 = not state`) er **altid** matematisk garanteret; det er kun *timingen* af skiftet, der er uforudsigelig.
**Sværhedsgrad:** Det mest avancerede eksempel — kræver, at du kan forklare `random.random()` (returnerer et flydende tal mellem 0.0 og 1.0) og hvordan en sandsynlighedstærskel (threshold) fungerer.
**Brug til eksamen:** Sjældent krævet i en almindelig opgave, men perfekt hvis censor spørger "hvordan simulerer man en defekt/uregelmæssig komponent?".

---

## 4. Nyttige random-funktioner (opslagstabel)

| Funktion | Beskrivelse | Bruges i eksempel |
|---|---|---|
| `random.random()` | Flydende tal mellem 0.0 og 1.0 | 3.6 |
| `random.uniform(a, b)` | Flydende tal mellem a og b | 3.1, 3.2, 3.5 |
| `random.randint(a, b)` | Heltal mellem a og b (begge inklusive) | 3.4, 3.5 |
| `random.choice(liste)` | Vælger tilfældigt element fra en liste | 3.3 |

Husk `import random` øverst i filen — modulet er indbygget i MicroPython, men skal importeres eksplicit.

---

## 5. Opsummeringstabel — hvilket eksempel skal jeg bruge?

| # | Eksempel | Sværhedsgrad | Bevarer modfase strikt? | Bedst til |
|---|---|---|---|---|
| 2.1 | `modfase_med_2_leder.py` | Meget let | Ja | Basis-skabelon |
| 2.2 | `modfase_value_func.py` | Let | Ja (garanteret) | Vise "elegant" kode uden fejlrisiko |
| 2.3 | `modfase_list.py` | Let | Ja (garanteret) | Skalerbarhed / lister |
| 2.4 | `modfase_mellem_2_grupper_af_leder.py` | Middel | Ja | Udvidelse til flere LED'er/grupper |
| 2.5 | `modfase_pwm.py` | Svær | Ja (analog) | Avanceret bonus m. lysstyrke/PWM |
| 3.1 | Random blink-hastighed (fælles) | Let | Ja | **Anbefalet standardvalg** |
| 3.2 | Hver diode egen hastighed | Let–middel | Ja | Vise dybere forståelse af modfase |
| 3.3 | Tilfældig start-diode | Let | Ja | Alternativ variation |
| 3.4 | Random + knap (flimmer) | Middel | Nej (i flimmer-delen) | Bonusopgave / kontrast |
| 3.5 | Random antal blink + pause | Middel | Ja | Mønster med løkker + pause |
| 3.6 | Simuleret defekt modfase | Svær | Ja (i outputtet) | Avanceret bonus, sandsynlighed |

**Anbefaling til en klassisk eksamensopgave (fx 10–15 point):** Start med **2.1 eller 2.2** som basis, og hvis opgaven beder om ekstra kompleksitet/tilfældighed, byg videre med **3.1 eller 3.2**. De holder sig strengt til modfase-definitionen, men viser du kan integrere `random` uden at bryde kravet.

---

## 6. Sådan kan du ændre/udvide koden til eksamen

Her er konkrete idéer til, hvordan du kan tilpasse eksemplerne, hvis din opgave beder om noget specifikt:

- **"Tilføj en tredje tilstand/LED":** Brug `modfase_mellem_2_grupper_af_leder.py` som skabelon, eller udvid `modfase_list.py`'s liste med flere pins og en anden indekseringslogik.
- **"Gør mønsteret mere uforudsigeligt":** Byt fast `sleep(0.5)` ud med `random.uniform(min, max)` som i 3.1/3.2.
- **"Kombiner med en knap":** Brug strukturen fra 3.4 (`if button.value() == 0: ... else: ...`), men skift `random_flimmer()` ud med en anden funktion, der *også* er modfase, hvis du vil bevare modfase i begge tilstande.
- **"Vis at du forstår hvad modfase kræver":** Forklar eksplicit (som i 3.2), at det ikke handler om *ens timing*, men om at de to outputs **aldrig har samme værdi samtidig** — dette er den vigtigste pointe at kunne formulere mundtligt.
- **"Simuler en fejl/defekt komponent":** Brug 3.6's `random.random() > threshold`-mønster, og juster tærsklen (0.1 = 10 % fejlrate) efter behov.
- **"Gør koden mere robust/skalerbar":** Skift fra separate `p1`/`p0`-variabler til en `list` (2.3) eller `dict`, så koden er nemmere at udvide.
- **"Analog/blød overgang":** Brug PWM-eksemplet (2.5), hvis din opgave nævner lysstyrke, dæmpning eller "fade".

**Generelt tip til eksamen:** Uanset hvilket eksempel du vælger, så vær klar til mundtligt at forklare **hvorfor** det stadig er modfase — dvs. pege på den linje i koden, der *garanterer*, at de to outputs er hinandens modsætning (fx `p0.value(not state)` eller `p0.off()` lige efter `p1.on()`).

---

## 7. Bemærkning om dine filer

Du har to identiske kopier af "Tilfældigt valg af hvilken diode der starter" (én med `(1)` i filnavnet). De indeholder præcis samme kode — du kan trygt bruge/beholde kun én af dem.
