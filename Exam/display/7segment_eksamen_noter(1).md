# 7-segment display – Eksamensnoter (Embedded / Pico)

Baseret på **7_segment.pptx** og "Rocket launcher"-opgaven.

---

## 1. Hvad er et 7-segment display?

> Slides: *"7 segment består af 7 LED'er der kan tændes og slukkes uafhængig af hinanden."*

Et 7-segment display er altså **ikke** én komponent, men **7 (eller 8) almindelige LED'er**
sat sammen i ét hus, formet så de tilsammen kan danne cifrene 0-9 (og lidt bogstaver).

Segmenterne navngives altid ens, så man kan tale om dem uden at pege:

```
  ── a ──
 |       |
 f       b
 |       |
  ── g ──
 |       |
 e       c
 |       |
  ── d ──          (dp) = decimal point, den lille prik i hjørnet
```

Hvert segment er en selvstændig LED → hvert segment skal have **sit eget ben ud**
(a, b, c, d, e, f, g, evt. dp), og så deler alle segmenterne **ét fælles ben**
(fælles katode eller fælles anode — se punkt 3).

---

## 2. Modstande (strømbegrænsning)

> Slides: *"Lod segmentet i print pladen '220 Ohm'"*

Ligesom enhver anden LED **skal** hvert segment have en seriemodstand, ellers brænder
det (eller Pico'ens ben) sammen. Slides angiver **220 Ω** som den værdi der skal loddes
ind til 7-segment-displayet på jeres print.

Hvis der kun er **én** modstand pr. segment (7 stk. i alt) sidder den enten:
- mellem hvert GPIO-ben og hvert segment-ben (mest almindeligt), eller
- på det fælles ben (kun muligt hvis alle segmenter tændes med samme strøm ad gangen).

---

## 3. Fælles katode vs. fælles anode

Der findes to typer 7-segment displays, og man **skal** vide hvilken type man har,
før koden giver mening:

| Type              | Fælles ben forbindes til | Segment "tændt" når GPIO er... |
|--------------------|---------------------------|----------------------------------|
| Fælles **katode**  | GND (stel)                 | **HIGH (1)** |
| Fælles **anode**   | +3,3V                      | **LOW (0)** |

> Slides: *"find ud af hvilke ben der tilsluttet hvilke segmenter"* — det samme gør sig
> gældende for at finde ud af **hvilken type** display det er, og hvilket ben der er det
> fælles ben. Ligesom i Pico_print-slides om at teste enkelt-LED'er for korrekt polaritet
> (`stel`-testopstillingen), kan man teste ét segment ad gangen med en modstand + 3,3V/GND
> for at se hvilken polaritet der tænder det.

I kode håndteres forskellen med én enkelt konstant, så resten af koden er ens uanset type:

```python
SEGMENT_ON = 1          # sæt til 1 hvis fælles KATODE
SEGMENT_OFF = 0 if SEGMENT_ON == 1 else 1   # regner automatisk det modsatte
```

I det færdige modul (punkt 5) bruges `.on()`/`.off()` i stedet for `SEGMENT_ON`/`SEGMENT_OFF`,
fordi displayet på BBB'en er testet til at være **fælles katode** (segment tændt = HIGH).

---

## 3a. Jeres faktiske pin-opsætning (Big Beautiful Board)

Dette er den rigtige, testede pin-mapping for 7-segment-displayet på BBB'en
(matcher silketrykket på printet):

| Segment       | GPIO |
|---------------|:----:|
| A (top)          | 12 |
| B (top right)    | 13 |
| C (bottom right) | 14 |
| D (bottom)       | 8  |
| E (bottom left)  | 9  |
| F (top left)     | 11 |
| G (middle)       | 10 |
| DP (prik)        | 15 |

---

## 4. Hvilke segmenter skal lyse for hvert ciffer?

> Slides: *"Opgaven skal laves med et python-modul som indeholder de 10 tal"*

Det "python-modul med de 10 tal" er i praksis en **opslagstabel (dictionary)**, der siger
hvilke segmenter der skal tændes for hvert ciffer 0-9:

| Ciffer | Tændte segmenter |
|--------|------------------|
| 0      | a b c d e f      |
| 1      | b c              |
| 2      | a b d e g        |
| 3      | a b c d g        |
| 4      | b c f g          |
| 5      | a c d f g        |
| 6      | a c d e f g      |
| 7      | a b c            |
| 8      | a b c d e f g (alle) |
| 9      | a b c d f g      |

I kode:

```python
CIFRE = {
    0: "abcdef",
    1: "bc",
    2: "abdeg",
    3: "abcdg",
    4: "bcfg",
    5: "acdfg",
    6: "acdefg",
    7: "abc",
    8: "abcdefg",
    9: "abcdfg",
}
```

**Sådan læses tabellen til eksamen:** tegn selv 7-segment-figuren fra punkt 1, og tjek
manuelt hvilke streger der SKAL være tændt for at tegne fx et "2" — det er sådan
tabellen er lavet, ikke udenad.

---

## 5. Modulet – `seven_segment_digits.py`

I stedet for at skrive pin-opsætning og ciffer-tabel ind i hvert eneste program,
samles det i **ét modul** som andre programmer bare kan `import`ere. Det er det,
slides mener med *"Opgaven skal laves med et python-modul som indeholder de 10 tal"*.

```python
"""
seven_segment_digits.py
Module for driving the single 7-segment display on the Big Beautiful Board
(Raspberry Pi Pico WH). Import this from another program to show digits
0-9 without re-typing the pin and segment setup every time.
Segment -> GPIO pin map (matches the silkscreen / your working test code):
    A (top)           -> GPIO 12
    B (top right)     -> GPIO 13
    C (bottom right)  -> GPIO 14
    D (bottom)        -> GPIO 8
    E (bottom left)   -> GPIO 9
    F (top left)      -> GPIO 11
    G (middle)        -> GPIO 10
    DP (dot)          -> GPIO 15
"""
from machine import Pin

SEGMENT_PINS = {
    'A': Pin(12, Pin.OUT),
    'B': Pin(13, Pin.OUT),
    'C': Pin(14, Pin.OUT),
    'D': Pin(8, Pin.OUT),
    'E': Pin(9, Pin.OUT),
    'F': Pin(11, Pin.OUT),
    'G': Pin(10, Pin.OUT),
    'DP': Pin(15, Pin.OUT),
}

# Which segments must be ON to draw each digit, 0-9.
DIGITS = {
    0: ('A', 'B', 'C', 'D', 'E', 'F'),
    1: ('B', 'C'),
    2: ('A', 'B', 'D', 'E', 'G'),
    3: ('A', 'B', 'C', 'D', 'G'),
    4: ('B', 'C', 'F', 'G'),
    5: ('A', 'C', 'D', 'F', 'G'),
    6: ('A', 'C', 'D', 'E', 'F', 'G'),
    7: ('A', 'B', 'C'),
    8: ('A', 'B', 'C', 'D', 'E', 'F', 'G'),
    9: ('A', 'B', 'C', 'D', 'F', 'G'),
}


def clear():
    """Turn every segment, including the dot, off."""
    for pin in SEGMENT_PINS.values():
        pin.off()


def show_digit(number, dot=False):
    """Light up the segments needed to show `number` (0-9 only)."""
    if number not in DIGITS:
        raise ValueError("show_digit only accepts whole numbers 0-9")
    clear()
    for seg in DIGITS[number]:
        SEGMENT_PINS[seg].on()
    if dot:
        SEGMENT_PINS['DP'].on()


# Quick self-test: running this file directly (not importing it)
# flashes through 0-9 once, so you can check the wiring is right.
if __name__ == "__main__":
    from time import sleep
    for n in range(10):
        show_digit(n)
        sleep(0.5)
    clear()
```

**Gennemgang:**
- `SEGMENT_PINS` binder hvert segment-bogstav (`'A'`-`'G'`, `'DP'`) til det **faktiske**
  GPIO-ben på BBB'en — denne mapping er testet og rigtig, så den skal I ikke selv finde.
- `DIGITS` er selve opslagstabellen: en tuple af hvilke segment-bogstaver der skal
  tændes for hvert ciffer 0-9 — samme indhold som tabellen i punkt 4, bare som tuples
  i stedet for strenge.
- `clear()` er en lille hjælpefunktion der slukker **alt**, inkl. `DP`-prikken.
- `show_digit(number, dot=False)`:
  1. Tjekker at `number` rent faktisk er et gyldigt ciffer (0-9) — ellers `raise ValueError`,
     i stedet for stille at vise noget forkert (eller crashe grimt længere nede).
  2. Kalder `clear()` **først**, så gamle segmenter fra sidste ciffer ikke bliver hængende.
  3. Tænder kun de segmenter det nye ciffer faktisk skal bruge.
  4. Tænder `DP` også, hvis `dot=True` er givet med.
- `if __name__ == "__main__":` er en klassisk Python-ting: koden herunder kører **kun**
  hvis man kører **selve** `seven_segment_digits.py` direkte (fx til at teste ledningerne) —
  den kører **ikke** når filen bliver importeret af et andet program. Det er derfor
  modulet kan bruges som ren "værktøjskasse" uden at et selvtest-blink starter hver gang.

### Sådan bruges modulet – "Rocket launcher" nedtælling

Fordi al pin- og tabel-opsætning nu ligger i modulet, bliver selve hovedprogrammet
meget kortere:

```python
from seven_segment_digits import show_digit, clear
from time import sleep


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


start_tal = get_int("Start nedtælling fra (0-9): ", 0, 9)

try:
    for tal in range(start_tal, -1, -1):
        show_digit(tal)
        print(tal)
        sleep(1)
    print("Affyring!")
    sleep(2)
    clear()
except KeyboardInterrupt:
    clear()
    print("Stoppet.")
```

Bemærk hvor lidt der er tilbage i hovedprogrammet: ingen `Pin()`-opsætning, ingen
`DIGITS`-tabel — bare `import` af modulet og selve nedtællings-logikken. Det er hele
pointen med at samle det i et modul: **genbrug** uden at skulle skrive pin-opsætningen
og ciffer-tabellen ind i hvert nyt program igen.

Statemachine-bemærkning: selve nedtællingen her er stadig en simpel `for`-løkke,
ikke en `state = state()`-maskine (modsat lyskryds-eksemplerne), fordi rækkefølgen
er fast og kendt på forhånd (9,8,7,...,0).

---

## 6. Hurtige facts til eksamen

- Et 7-segment display = 7 (eller 8 med `DP`) uafhængige LED'er i ét hus.
- Segmenterne hedder altid **A, B, C, D, E, F, G** (med `DP` som decimal-punktet).
- **Fælles katode** → segment tændes med **HIGH** (`.on()`). **Fælles anode** → segment tændes med **LOW**.
- BBB'ens display er **fælles katode**, koblet på GPIO 12,13,14,8,9,11,10,15 (A-G, DP).
- Hvert segment skal have sin egen strømbegrænsende modstand (**220 Ω** ifølge slides).
- Cifferets segment-mønster (0-9) findes via en **opslagstabel** (`DIGITS`-dictionary med tuples), ikke ved beregning.
- Saml pin-opsætning + tabel i **ét modul** (`seven_segment_digits.py`) og `import`ér det derfra, i stedet for at gentage koden i hvert program — det er pointen med "et python-modul som indeholder de 10 tal" fra slides.
- `if __name__ == "__main__":` gør at et modul kan have sin egen indbyggede selvtest, uden at testen kører når andre programmer importerer det.
- `show_digit()` bør altid kalde `clear()` først, så det forrige ciffers segmenter ikke bliver hængende.
- Husk at slukke alle segmenter ved programstop (`except KeyboardInterrupt` → `clear()`), så displayet ikke hænger fast på et tal.
