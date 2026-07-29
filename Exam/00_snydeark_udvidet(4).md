# Snydeark til reeksamen — Embedded systemer

## Pin-layout på dit print (ITEK 1. Semester)

**Trafiklys-LED'er (venstre/højre retning):**

| Variabel | GPIO | Farve/retning |
|---|---|---|
| `ledRL` | 0 | Rød, venstre |
| `ledYL` | 1 | Gul, venstre |
| `ledGL` | 2 | Grøn, venstre |
| `ledRR` | 3 | Rød, højre |
| `ledYR` | 4 | Gul, højre |
| `ledGR` | 5 | Grøn, højre |

```python
ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)

ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)
```

**7-segment display:**

| Variabel | GPIO | Position på displayet | Standard segment |
|---|---|---|---|
| `led1` | 8 | bund | d |
| `led2` | 9 | bund-venstre | e |
| `led3` | 10 | midt | g |
| `led4` | 11 | top-venstre | f |
| `led5` | 12 | top | a |
| `led6` | 13 | top-højre | b |
| `led7` | 14 | bund-højre | c |
| `led8` | 15 | punktum | dp |

```python
led1 = Pin(8, Pin.OUT)   # bund
led2 = Pin(9, Pin.OUT)   # bund-venstre
led3 = Pin(10, Pin.OUT)  # midt
led4 = Pin(11, Pin.OUT)  # top-venstre
led5 = Pin(12, Pin.OUT)  # top
led6 = Pin(13, Pin.OUT)  # top-højre
led7 = Pin(14, Pin.OUT)  # bund-højre
led8 = Pin(15, Pin.OUT)  # punktum
```

Segment-navngivning til reference:
```
    _a_
   f   b
    _g_
   e   c
    _d_
```

**Knapper:**

| Variabel | GPIO | Funktion |
|---|---|---|
| `btn_up` | 6 | fx "op"/"start"/"næste" |
| `btn_down` | 7 | fx "ned"/"stop"/"forrige" |

```python
btn_up = Pin(6, Pin.IN, Pin.PULL_UP)
btn_down = Pin(7, Pin.IN, Pin.PULL_UP)
```

**ADC-indgang:** potmeter/spænding læses på `Pin(26)` (ADC0) — det er
fast på Pico'en og gælder uanset print.

```python
from machine import ADC
pot = ADC(Pin(26))
```

---

## Guide: sådan skriver du et simpelt program fra bunden

Alle opgaverne bygger i bund og grund på den samme opskrift. Her er
den, trin for trin, med et konkret eksempel: en LED der blinker ved
hjælp af PWM.

**Trin 1 — Importér det du skal bruge.**
Næsten alle programmer starter med de samme to linjer:
```python
from machine import Pin, PWM
from time import sleep
```
`machine` giver dig adgang til selve hardwaren (ben, PWM, ADC).
`time` giver dig `sleep()`, som du bruger til at vente et antal
sekunder mellem hver handling.

**Trin 2 — Opret dine pins.**
Bestem hvilket ben du vil styre, og lav et Pin/PWM-objekt for det —
brug pin-layoutet øverst i dette dokument, så du ikke selv skal
huske GPIO-numrene:
```python
led = PWM(Pin(2))   # ledGL fra dit print
```

**Trin 3 — Sæt PWM-frekvensen (kun hvis du bruger PWM).**
Dette er den interne switching-frekvens PWM'en bruger til at dæmpe
lyset — sæt den én gang, typisk 1000 Hz:
```python
led.freq(1000)
```

**Trin 4 — Skriv selve løkken.**
Det er her opgaven bliver løst. En simpel blink-løkke:
```python
while True:
    led.duty_u16(65535)   # fuldt tændt (100%)
    sleep(0.5)
    led.duty_u16(0)       # slukket (0%)
    sleep(0.5)
```

**Trin 5 — Saml det hele, og husk oprydning.**
Sæt det hele ind i et `try/except`, så du kan stoppe programmet
pænt med Ctrl+C uden at LED'en bliver hængende tændt:
```python
from machine import Pin, PWM
from time import sleep

led = PWM(Pin(2))
led.freq(1000)

try:
    while True:
        led.duty_u16(65535)
        sleep(0.5)
        led.duty_u16(0)
        sleep(0.5)

except KeyboardInterrupt:
    led.duty_u16(0)
    led.deinit()
    print("Stoppet.")
```

Det er hele opskriften: **importér → opret pins → (evt. sæt
frekvens) → while-løkke der gør arbejdet → try/except til
oprydning.** Skal du bruge en knap i stedet for bare tid, erstatter
du blot betingelsen i løkken:
```python
if btn_up.value() == 0:   # husk: PULL_UP betyder tryk = 0
    led.duty_u16(65535)
```
Og skal du bruge flere "faser" (grøn->gul->rød, elevator-etager
osv.), erstatter du while-løkken med statemachine-skabelonen længere
nede i dette dokument.

---

## Skabelonen du kan genbruge til næsten alt

**Input med validering** (brug den til alle "spørg brugeren om et tal"-opgaver):
```python
def get_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"> Indtast en værdi mellem {low} og {high}:")
        except ValueError:
            print("> FEJL. Indtast et helt tal.")
```

**Statemachine** (brug den til trafiklys, elevator, hysterese, alt der har "faser"):
```python
def state_a():
    # gør noget
    sleep(1)
    return state_b        # returnér NÆSTE funktion, kald den ikke selv

def state_b():
    sleep(1)
    return state_a

state = state_a
while state:
    state = state()
```
Trick: hvis du er i tvivl om hvor mange states en opgave kræver, tegn
den som cirkler og pile FØRST (som slidesættet siger) — så bliver det
tydeligt hvilke funktioner du skal skrive.

**ADC -> spænding:**
```python
from machine import ADC, Pin
adc = ADC(Pin(26))
voltage = adc.read_u16() / 65535 * 3.3
```
Skal du måle mere end 3,3V (batteri, 12V osv.), husk spændingsdeler
FØR Pico'ens ben, og gang tilbage i koden:
```python
real_voltage = adc_voltage / (R2/(R1+R2))
```

**PWM -> lysstyrke/blink:**
```python
pwm = PWM(Pin(0))
pwm.freq(1000)                    # fast intern switching-frekvens
pwm.duty_u16(int(pct/100*65535))  # 0-100% lysstyrke
```

**Knap med PULL_UP** (tryk = 0, ikke 1):
```python
button = Pin(6, Pin.IN, Pin.PULL_UP)
if button.value() == 0:
    ...
```

## Generelle eksamens-tips (kun det praktiske, ikke pep-talk)

- Skriv `try / except KeyboardInterrupt:` rundt om hovedløkken og
  nulstil LED/PWM i except-blokken — det er i alle dine egne
  eksempler, så det forventes formentlig igen.
- `Pin.PULL_UP` betyder knappen læses som `0` når den er trykket —
  glem ikke det, det er den hyppigste fejl i knap-opgaver.
- Kend forskellen på `led.on()/off()` (digital ud) og
  `pwm.duty_u16(...)` (analog-agtig ud via PWM) — brug PWM når
  opgaven nævner "lysstyrke" eller "dæmpe", ellers almindelig Pin.
- Til statemachine-opgaver: tegn den (kurset nævner selv et
  tegneprogram) før du koder — så mapper hver cirkel direkte til én
  Python-funktion.
- Test ADC-koden med et potmeter FØR du stoler på en rigtig sensor —
  det er den hurtigste måde at se om din formel (u16 -> volt) er rigtig.

---

## Baggrundsviden fra slidesættene

### Mikroprocessor vs. mikrocontroller

| | Mikroprocessor | Mikrocontroller |
|---|---|---|
| Memory | Kræver ekstern hukommelse | Indbygget ROM/RAM på chippen |
| Perifere enheder | Kræver ekstra komponenter udenom | Indbygget (timere, I/O, ADC) |
| Clock speed | GHz-område | kHz-MHz-område |
| Strømforbrug | Højt, ingen power-saving mode | Lavt, har power-saving modes |
| Brug | Generel computerkraft (PC) | Kompakte, batteridrevne, logikstyring |
| Pris | Dyrere (flere komponenter) | Billigere (ét chip klarer det hele) |

Pico 2 W'en du bruger i faget er en **mikrocontroller** — det er derfor den har indbygget ADC, PWM og GPIO uden ekstra chips.

### Vigtige begreber (ordforklaring)

- **CPU** = Central Processing Unit, selve regneenheden.
- **Clock** = clockfrekvens i Hz — hvor mange "tick" processoren laver pr. sekund.
- **Kerne (core)** = antal uafhængige CPU'er i samme chip (dual-core, quad-core osv.).
- **Databus** = leder data ind/ud af CPU'en.
- **Adressebus** = leder informationen om HVOR i hukommelsen data skal læses/skrives.
- **ALU** = "regneenheden" inde i CPU'en, selve delen der udfører beregninger.

### Historisk tidslinje (hvis der kommer et historie-spørgsmål)

- **Intel 4004** (1971) — verdens første mikroprocessor, ca. 175 kHz.
- **Intel 8080** (1974) og **8085** (1976) — tidlige 8-bit processorer, 3-6 MHz, 8-bit databus, 16-bit adressebus.
- **Zilog Z80** — konkurrent til 8085, brugt i mange klassiske hjemmecomputere.
- **Intel Pentium 4** — ca. 1,8 GHz.
- **I dag**: AMD/Intel over 3 GHz, mange kerner.
- **Moore's lov**: antallet af transistorer på en chip fordobles ca. hvert 2. år (empirisk observation, ikke en fysisk lov).
- **Chip-fabrikanter** (som rent faktisk producerer/støber chippene): TSMC (Taiwan) og Samsung (Sydkorea) dominerer markedet.
- **Chip-leverandører 2021** (rangeret efter salg): Samsung, Intel, SK Hynix, Micron, Qualcomm, Nvidia, Broadcom, Texas Instruments, MediaTek, AMD.

### Hardware du har arbejdet med — nøgletal

**Raspberry Pi Pico 2 W**
([raspberrypi.dk](https://raspberrypi.dk/produkt/raspberry-pi-pico-2-w/)):
bygget på **RP2350**-chippen, dual-core (enten Arm Cortex-M33 @ 150
MHz eller valgfrit Hazard3 RISC-V-kerner), 520 kB SRAM, 4 MB flash,
indbygget 2,4 GHz trådløs (WiFi 802.11n + Bluetooth 5.2 via en
Infineon CYW43439-chip), 26 multifunktions-GPIO-ben, **3×12-bit
ADC**, SWD-debugport, TrustZone-sikkerhedsfunktioner. **Intet
styresystem** — den kører MicroPython direkte på "bare metal", helt
ligesom den oprindelige Pico.

> Bemærk: ADC'en er fysisk 12-bit, men MicroPythons `read_u16()`
> skalerer altid resultatet op til 16-bit (0-65535) — derfor deler
> man med 65535 og ikke 4095 i koden.

**Det håndloddede print** (ITEK 1. Semester) er bygget op omkring
Pico 2 W'en, med følgende komponenter:

- 1× Raspberry Pi Pico 2 W
- 2× rød LED-indikator ([Würth Elektronik 151051RS11000](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/151051RS11000/4490012))
- 2× gul LED-indikator ([Würth Elektronik 151051YS04000](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/151051YS04000/4490018))
- 2× grøn LED-indikator ([Würth Elektronik 151051VS04000](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/151051VS04000/4490015))
- 4× 330 Ω modstand ([Yageo MFR-25FRF52-330R](https://www.digikey.com/en/products/detail/yageo/MFR-25FRF52-330R/9139001))
- 2× 220 Ω modstand ([KOA Speer CF1-2CT52R221J](https://www.digikey.com/en/products/detail/koa-speer-electronics-inc/CF1-2CT52R221J/13537410))
- 2× trykknap ([Adafruit 367](https://www.digikey.com/en/products/detail/adafruit-industries-llc/367/10669771))
- 2× Phoenix Contact MKDS 1/10-3,5-serien printklemme ([RS Delivers](https://export.rsdelivers.com/product/phoenix-contact/1751329/phoenix-contact-mkds-1/10-35-series-pcb-terminal-block-10-contact-35mm-1/1703807))

Bemærk modstandsværdierne: 330 Ω bruges typisk til de 4 LED'er på
trafiklys-delen af printet, mens 220 Ω-modstandene passer bedre til
7-segment-displayets segmenter (lavere modstand = mere strøm/lys pr.
segment, hvilket er nødvendigt fordi hvert segment er en lille LED
der skal være tydeligt synlig).

### Netværksværktøjer (hvis der kommer spørgsmål om opsætning)

- **Putty**: SSH/Telnet-klient — bruges til at logge ind på en Raspberry Pi/enhed over netværket via kommandolinje.
- **VNC (RealVNC)**: fjernskrivebordsprogram — giver et grafisk skrivebord til en headless Raspberry Pi.
- **Advanced IP Scanner**: scanner et helt IP-range (fx `10.110.0.1-10.110.0.254`) og viser hvilke enheder der er på nettet med IP, MAC-adresse og producent — bruges til at finde din Pi/Pico's IP-adresse på netværket.

### PWM (Pulse Width Modulation) — teori

- PWM regulerer effektivt lysstyrke/effekt ved hurtigt at tænde og slukke et signal.
- **Duty cycle** = forholdet (i %) mellem "on"-tid og "off"-tid indenfor én periode. 50% duty cycle = tændt halvdelen af tiden.
- Skelnen der er nem at glemme: PWM-**carrier**-frekvensen (`pwm.freq(1000)`) er den interne, hurtige switching-frekvens der bruges til selve dæmpningen — den er IKKE det samme som en blinkefrekvens du selv styrer med `sleep()` i en løkke udenom.

### ADC (Analog-til-Digital konvertering) — teori

- Omdanner et analogt spændingssignal til en digital værdi mikrocontrolleren kan regne videre på.
- Pico'ens ADC måler kun 0-3,3V. Skal du måle en højere spænding (fx et 6,4-8,4V robotbatteri, eller 0-12V), skal du bruge en **spændingsdeler** (to modstande) FØR signalet rammer ADC-indgangen, og så regne den rigtige spænding ud igen i softwaren.
- ADC-indgangen på Pico'en, du typisk bruger i opgaverne, sidder på **GPIO 26 (ADC0)**.

### Multimeter / voltmeter — teori

Et multimeter kan måle tre ting:
1. **Spænding** (potentialeforskel mellem to punkter).
2. **Strøm** (hvor meget strøm der løber gennem kredsløbet).
3. **Modstand** (bruges til at teste komponenter/kredsløb).

Et voltmeter bygget med Pico'en er i praksis "ADC + en formel + en måde at vise resultatet på" (konsol-print, LED-bargraf eller 7-segment).

### Statemachine — teori

- En statemachine strukturerer en proces som en række **states** (tegnes som cirkler), med pile der viser hvilken state man skifter til og hvorfor.
- I koden svarer hver cirkel til én funktion. Funktionen udfører sit arbejde og **returnerer** (ikke kalder) den næste state-funktion.
- **Hysterese-sløjfe**: bruges når man vil undgå at noget tænder/slukker for tit omkring ét enkelt "sætpunkt" (fx en termostat). I stedet for ét sætpunkt bruges to grænser — en "on"-grænse og en (højere) "off"-grænse — så systemet ikke "flimrer".

### Farvet konsoloutput (ANSI escape-koder)

Set flere gange i statemachine-slidesættet til at farve tekst i terminalen — nyttigt hvis en opgave vil have "grønt lys = grøn tekst" i konsollen:
```python
print('\x1b[7;32;40m' + "Grøn! Kør" + '\x1b[0m')   # grøn baggrund/tekst
print('\x1b[6;30;43m' + "Gul! stop" + '\x1b[0m')   # gul
print('\x1b[6;30;41m' + "Rød! stop" + '\x1b[0m')   # rød
```
Formatet er `\x1b[<stil>;<forgrund>;<baggrund>m` og nulstilles altid med `\x1b[0m` bagefter, ellers "smitter" farven resten af outputtet.

### GY-53 ToF-afstandssensor — teori

- Time-of-Flight-sensor (baseret på VL53L0X-chippen), måleområde 0-2 meter.
- Kan sende data på tre måder: UART, **PWM** eller I²C.
- I PWM-mode sender sensoren et signal med fast periode (~22 ms), og **pulslængden (HIGH-tiden) er proportional med afstanden**:
  ```
  Afstand (mm) = Pulslængde (µs) / 10
  ```
- Fordel ved PWM-mode: simpel implementering, ingen adressering nødvendig. Ulempe: mindre robust mod støj, kræver præcis timing (derfor bruges `time.ticks_us()` og `ticks_diff()`, ikke almindelig `time.time()`).

### 7-segment display — teori

- Består af 7 uafhængige LED'er (segmenterne a-g) der tændes i forskellige kombinationer for at danne cifre 0-9, plus evt. et 8. "segment" (decimalpunktet).
- Hvert segment skal have sin egen 220 Ω modstand for ikke at trække for meget strøm.
- Praktisk tommelfingerregel: gem cifferkombinationerne (0-9) i et separat Python-modul du kan importere, i stedet for at skrive dem ind i hovedprogrammet hver gang — nemmere at genbruge og nemmere for censor at læse.
