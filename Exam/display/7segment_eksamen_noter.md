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

## 5. Fuld kode – "Rocket launcher" nedtælling

Dette er opgaven fra slides: i stedet for at skrive nedtællingen på skærmen med `print()`,
skal den vises på selve 7-segment-displayet.

```python
from machine import Pin
from time import sleep

SEGMENT_ON = 1
SEGMENT_OFF = 0 if SEGMENT_ON == 1 else 1

segmenter = {
    "a": Pin(10, Pin.OUT), "b": Pin(11, Pin.OUT), "c": Pin(12, Pin.OUT),
    "d": Pin(13, Pin.OUT), "e": Pin(14, Pin.OUT), "f": Pin(15, Pin.OUT),
    "g": Pin(16, Pin.OUT),
}

CIFRE = {
    0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg",
    5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg",
}


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


def vis_ciffer(tal):
    tal = tal % 10
    aktive = CIFRE[tal]
    for navn, pin in segmenter.items():
        pin.value(SEGMENT_ON if navn in aktive else SEGMENT_OFF)


def sluk_alt():
    for pin in segmenter.values():
        pin.value(SEGMENT_OFF)


start_tal = get_int("Start nedtælling fra (0-9): ", 0, 9)

try:
    for tal in range(start_tal, -1, -1):
        vis_ciffer(tal)
        print(tal)
        sleep(1)
    print("Affyring!")
    sleep(2)
    sluk_alt()
except KeyboardInterrupt:
    sluk_alt()
    print("Stoppet.")
```

**Gennemgang:**
- `segmenter` er en dictionary der binder hvert segment-navn til det faktiske GPIO-ben
  (**ret pin-numrene til jeres egen lodning** — det er det slides mener med at "finde ud af
  hvilke ben der er tilsluttet hvilke segmenter").
- `vis_ciffer(tal)` slår cifferet op i `CIFRE`, og tænder/slukker hvert segment ud fra
  om dets bogstav (a-g) indgår i strengen for det tal.
- `tal % 10` er en lille sikkerhed, så funktionen aldrig crasher hvis den kaldes med
  et tal uden for 0-9.
- `sluk_alt()` bruges både efter nedtællingen er færdig, og i `except KeyboardInterrupt`,
  så displayet ikke "hænger" med et tændt tal når programmet stoppes.
- Selve nedtællingen er en simpel `for`-løkke — bemærk at det **ikke** er en
  statemachine med `state = state()` her (modsat lyskryds-eksemplerne), fordi
  rækkefølgen er fast og kendt på forhånd (9,8,7,...,0). Det kunne dog nemt laves om
  til statemachine-stil, hvis opgaven kræver det.

---

## 6. Hurtige facts til eksamen

- Et 7-segment display = 7 (eller 8 med `dp`) uafhængige LED'er i ét hus.
- Segmenterne hedder altid **a, b, c, d, e, f, g** (med `dp` som decimal-punktet).
- **Fælles katode** → segment tændes med **HIGH**. **Fælles anode** → segment tændes med **LOW**.
- Hvert segment skal have sin egen strømbegrænsende modstand (**220 Ω** ifølge slides).
- Cifferets segment-mønster (0-9) findes normalt via en **opslagstabel/dictionary**, ikke ved beregning.
- Test altid polaritet/type (katode vs. anode) og pin-tilslutning **før** koden skrives — akkurat som man tester en enkelt LED's polaritet, jf. Pico_print-slides.
- Husk at slukke alle segmenter ved programstop (`except KeyboardInterrupt` → `sluk_alt()`), så displayet ikke hænger fast på et tal.
