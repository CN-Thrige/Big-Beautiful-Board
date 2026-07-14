# PWM – Eksamensnoter (Embedded / Pico)

Baseret på **PWM.pptx** og jeres egen kode (LED-dæmper med blink-frekvens + lysstyrke).

---

## 1. Hvad er PWM?

**PWM = Pulse Width Modulation** (Puls-Bredde-Modulation).

> Slides' egen formulering: *"Hvordan regulerer man lysstyrken på en LED?"*

En digital pin kan kun være **HIGH** eller **LOW** – den kan ikke give "halv spænding".
PWM løser det ved at tænde/slukke pinden **meget hurtigt**, og variere **hvor stor en
andel af tiden** den er tændt. Øjet (og de fleste sensorer/motorer) kan ikke følge med
i den hurtige switching, og opfatter i stedet et **gennemsnit** — det er det, der opleves
som en dæmpet lysstyrke.

```
HIGH  ──┐   ┌──┐   ┌──┐   ┌──
        │   │  │   │  │   │
LOW     └───┘  └───┘  └───┘
        <-- én periode -->
```

---

## 2. Duty Cycle

> Slides: *"Duty Cycle. Benyttes % til at beskrive forholdet mellem on og off."*

**Duty cycle** = hvor stor en procentdel af én periode signalet er HIGH.

```
Duty cycle (%) = (tid HIGH / hele periodens tid) × 100
```

| Duty cycle | LED opleves som |
|-----------|------------------|
| 0 %       | Helt slukket |
| 25 %      | Svagt lys |
| 50 %      | Middel lys |
| 100 %     | Fuldt tændt (som almindeligt digitalt HIGH) |

**På Pico'en i MicroPython** styres duty ikke direkte i %, men som et 16-bit tal
via `duty_u16()`:

```python
duty_u16 range:  0        -> 0 %   (altid slukket)
                 65535    -> 100 % (altid tændt)
```

Omregning fra procent til `duty_u16`-værdien (præcis som i jeres kode):

```python
duty = int(brightness_pct / 100 * 65535)
```

---

## 3. To forskellige "frekvenser" – den vigtigste faldgrube til eksamen!

Jeres kode har **to helt forskellige frekvens-begreber**, og det er nemt at forveksle dem:

| Navn i koden      | Værdi          | Hvad styrer den?                                   | Kan øjet se den? |
|-------------------|----------------|-----------------------------------------------------|-------------------|
| `PWM_CARRIER`     | 1000 Hz (fast) | Den interne switching-frekvens PWM'en bruger til at lave **dæmpning** (duty cycle) | Nej – alt for hurtig |
| `frequency`       | 0-20 Hz (bruger-valgt) | Hvor tit LED'en **blinker synligt** tændt/slukket | Ja – det er meningen |

Med andre ord:
- `PWM_CARRIER` (1000 Hz) er "usynlig" og bruges **udelukkende** til selve lysstyrke-reguleringen (duty cycle).
- `frequency` (0-20 Hz) er en **software-timer** ovenpå PWM'en, der tænder/slukker hele PWM-signalet med `sleep()` — det er det, man rent faktisk ser blinke.

Det er derfor koden både har `led_pwm1.freq(PWM_CARRIER)` (sat once, i opsætningen)
**og** en separat `half_period`-beregning ud fra `frequency` (brugerens blink-ønske).

---

## 4. Koden – linje for linje

```python
from machine import Pin, PWM
from time import sleep

led_pwm1 = PWM(Pin(0))   # red
led_pwm2 = PWM(Pin(1))   # yellow
PWM_CARRIER = 1000       # fast intern switching-frekvens, bruges kun til dæmpning
led_pwm1.freq(PWM_CARRIER)
led_pwm2.freq(PWM_CARRIER)
```
- `PWM(Pin(0))` opretter et PWM-objekt på pin 0 (og pin 1).
- `.freq(1000)` sætter selve PWM-signalets grundfrekvens — høj nok til at være usynlig,
  men lav nok til at Pico'en nemt kan lave den.

```python
def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")
```
- Robust input-funktion: bliver ved med at spørge indtil brugeren taster et **helt tal**
  **inden for et gyldigt interval** (`lo`-`hi`). Fanger både forkerte typer (`ValueError`)
  og tal uden for grænsen.

```python
frequency = get_int("Blink frequency (0-20 Hz, 0 = no blinking): ", 0, 20)
brightness_pct = get_int("Brightness (0-100%): ", 0, 100)
duty = int(brightness_pct / 100 * 65535)
```
- Brugeren vælger blink-frekvens (0-20 Hz) og lysstyrke (0-100 %).
- `duty` beregnes **én gang** ud fra lysstyrken — det er den værdi der bruges hver gang
  LED'en skal være "tændt".

```python
def set_leds(on):
    d = duty if on else 0
    led_pwm1.duty_u16(d)
    led_pwm2.duty_u16(d)
```
- Lille hjælpefunktion: `on=True` → sæt til den valgte lysstyrke. `on=False` → helt slukket (0).
- Bemærk: den regulerer **begge** LED'er samtidig med samme duty.

```python
try:
    if frequency == 0:
        set_leds(True)          # solid, ved valgt lysstyrke (0% = slukket)
        while True:
            sleep(1)
    else:
        half_period = (1 / frequency) / 2
        while True:
            set_leds(True)
            sleep(half_period)
            set_leds(False)
            sleep(half_period)
```
- **`frequency == 0`** → intet blink ønsket: LED sættes fast til den valgte lysstyrke,
  og programmet "venter" bare (i en uendelig løkke) — der sker ikke mere før `Ctrl+C`.
- **`frequency > 0`** → blink ønsket:
  - `half_period = (1 / frequency) / 2` — udregner **halvdelen** af én hel blink-periode.
    Hvis fx `frequency = 2 Hz`, er én hel periode `0,5 s`, så `half_period = 0,25 s`
    (LED tændt i 0,25 s, slukket i 0,25 s → 2 hele blink pr. sekund).
  - Selve blinket er en **2-state statemachine**: `tændt → (vent half_period) → slukket → (vent half_period) → tændt → ...`

```python
except KeyboardInterrupt:
    led_pwm1.duty_u16(0)
    led_pwm2.duty_u16(0)
    led_pwm1.deinit()
    led_pwm2.deinit()
    print("Stopped, PWM deinitialized.")
```
- Når man stopper programmet (`Ctrl+C`), er det vigtigt at:
  1. Sætte duty til 0 (slukke LED'erne helt), og
  2. Kalde `.deinit()` på hver PWM — det frigiver PWM-hardwaren/kanalen igen,
     så den ikke "sidder fast" og forstyrrer næste program der vil bruge samme pin.
  - **Til eksamen:** glemmer man `deinit()`, kan pinnen stadig opføre sig som PWM
    næste gang man prøver at bruge den som almindelig `Pin.OUT` — en klassisk fejlkilde.

---

## 5. Praktisk opsætning (Probe / oscilloskop)

> Slides nævner brug af en **probe** til at måle PWM-signalet direkte på pin'en.

- En probe/oscilloskop viser signalet som spænding over tid, så man visuelt kan se
  **duty cycle** (bredden af de høje "pulser") og **periodetid** (afstanden mellem dem).
- Til eksamen: kunne blive bedt om at aflæse duty cycle fra et billede af et
  oscilloskop-signal — brug formlen fra afsnit 2 (tid HIGH ÷ hele perioden × 100).

---

## 6. Opgave fra slides: knap op/ned for lysstyrke

> Slides: *"Brug knapperne til skrue op og ned for LED'en"*

Med boardets pin-layout:

```python
button1 = Pin(6, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)
```

Idé: i stedet for at spørge om lysstyrke med `get_int` én gang ved opstart, læses
knapperne løbende i en `while True`-løkke:
- `button1` trykket (værdi `0`, pga. `PULL_UP`) → `brightness_pct += trin`
- `button2` trykket → `brightness_pct -= trin`
- Ny `duty_u16()`-værdi sættes hver gang, og den nye % printes til skærmen.

Dette er den samme kerne-logik som `set_leds()`/`duty`-beregningen ovenfor — bare
styret af knap-input i stedet for ét fast valg ved start.

---

## 7. Hurtige facts til eksamen

- **PWM** = Pulse Width Modulation.
- **Duty cycle** = andelen af perioden hvor signalet er HIGH (i %).
- `duty_u16()` går fra **0** (0 %) til **65535** (100 %) på Pico'en.
- Formel: `duty = int(procent / 100 * 65535)`.
- Der er **to adskilte frekvenser** i jeres kode: `PWM_CARRIER` (fast, usynlig,
  kun til dæmpning) og `frequency` (bruger-valgt, synligt blink via `sleep`).
- `half_period = (1 / frequency) / 2` — tiden for hhv. tændt og slukket del af ét blink.
- Husk **`deinit()`** når et PWM-objekt ikke skal bruges mere.
- `frequency == 0` betyder "ingen blinking" — LED lyser solidt ved den valgte lysstyrke
  (0 % lysstyrke = helt slukket, men stadig "solid state", ikke blinkende).
