# Eksamenseksempler – Komplet Gennemgang (10, 20, 25 og 30 point)

Denne guide gennemgår alle dine eksamens-kodefiler: hvad de gør, hvorfor de scorer som de gør, og – vigtigst – **hvilke fejl der kostede point**, så du kan undgå dem selv.

---

## 1. Eksamensspørgsmålene (kontekst)

Fra `modfase_forklaring_med_eksempler.md` er de oprindelige krav:

> **Opgave 2 (10 point):** Tilføj endnu en lysdiode og modificér programmet, så Pin1-dioden fortsætter med at blinke, og den tilføjede lysdiode blinker i **modfase** med den første diode (den ene er slukket, mens den anden lyser, og omvendt).
>
> **Opgave 3 (15 point):** Tilføj en knap, så:
> - **a.** Mens knappen er trykket ned → lysdioderne blinker **i takt** (synkront).
> - **b.** Når knappen er sluppet → lysdioderne blinker i **modfase**.

Alle eksempler herunder er forsøg på at løse varianter af denne opgave – med stigende kompleksitet og pointværdi.

---

## 2. De tre "reeksamen"-niveauer (fra .md-filen)

### 2.1 — 10 point: Grundlæggende modfase (uden knap)

```python
from machine import Pin
from time import sleep

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    p0.on()
    sleep(0.5)
    p0.off()
    p1.on()
    sleep(0.5)
    p1.off()
```

**Hvad den gør:** `p0` tændes i 0.5 sek., slukkes; derefter tændes `p1` i 0.5 sek., slukkes. Fordi `p1` allerede var slukket, mens `p0` var tændt (og omvendt bagefter), opstår modfase-mønsteret **selvom det er skrevet sekventielt** (den ene "on" og den anden "off" sker lige efter hinanden uden mellemrum).

**Hvorfor kun 10 point:** Løsningen opfylder kun opgave 2 (den simple modfase-udvidelse). Der er **ingen knap**, og dermed **ingen "i takt"-tilstand** — hvilket var opgave 3's krav. Det er en korrekt, men minimal løsning.

**Bemærk:** I den oprindelige `.md`-fil var koden indrykket forkert (ekstra mellemrum før `while True:`), hvilket ville give en `IndentationError` i Python. Det er sandsynligvis en kopierings-fejl i dokumentet, ikke i den faktiske eksamenskode.

---

### 2.2 — 20 point: Med knap, men uden rigtig "i takt"/modfase-opdeling

```python
from machine import Pin
from time import sleep

button1 = Pin(6, Pin.IN, Pin.PULL_UP)

p1 = Pin(0, Pin.OUT)  #red
p0 = Pin(1, Pin.OUT) #yellow

while True:
    if button1.value() == 0:
        p0.on()
        sleep(0.5)
        p0.off()

        p1.on()
        sleep(0.5)
        p1.off()
```

**Hvad den gør:** Der er nu en knap (`button1`), men den styrer kun **om** blink-sekvensen kører overhovedet — ikke to forskellige mønstre. Når knappen er trykket (`value() == 0`, fordi `PULL_UP` betyder "trykket = lav spænding"), køres den samme sekventielle gul→rød-blink som i 10-points-eksemplet. Når knappen **ikke** er trykket, sker der intet — begge LED'er er slukkede.

**Hvorfor kun 20 point (og ikke fuld pointsum):**
1. **Mangler "i takt"-tilstanden.** Opgaven kræver, at LED'erne blinker *synkront* når knappen er trykket — men her sker der stadig kun modfase-blink, blot betinget af knappen.
2. **Ingen adfærd, når knappen er sluppet.** Ifølge opgaven skal modfase køre, når knappen er **sluppet** (`else`-gren mangler helt) — her er det omvendt og desuden ufuldstændigt: intet sker ved slip.
3. **`sleep()` blokerer knap-aflæsningen.** Fordi hele blink-sekvensen (i alt 1 sekund) ligger inde i `if`-blokken uden nye tjek af knappen undervejs, kan programmet ikke reagere øjeblikkeligt, hvis knappen slippes midt i en blink-cyklus.

**Hvordan man retter den op til fuld pointsum:** Tilføj en `else`-gren, der udfører selve modfase-mønsteret, og lav `if`-grenen til en ægte "i takt"-tilstand (begge `p0.on(); p1.on()` samtidig, så `off()` samtidig) — præcis som i 25-points-eksemplet nedenfor.

---

### 2.3 — 25 point: Korrekt opdeling af "i takt" og "modfase" via funktioner

```python
from machine import Pin
from time import sleep

button1 = Pin(6, Pin.IN, Pin.PULL_UP)

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

led = p1, p0


def task2():
    p0.on()
    sleep(0.5)
    p0.off()

    p1.on()
    sleep(0.5)
    p1.off()


def task3():
    if button1.value() == 0:
        p0.on()
        p1.on()

        sleep(0.5)

        p0.off()
        p1.off()
        sleep(0.5)

    else:
        task2()


while True:
    task3()
```

**Hvad den gør:**
- `task2()` = modfase-mønsteret (samme som 10-points-eksemplet).
- `task3()`: hvis knappen **er trykket** → begge LED'er tændes **samtidig**, holdes i 0.5 sek., slukkes **samtidig**, pause i 0.5 sek. → dette er **"i takt"**. Hvis knappen **ikke** er trykket → kald `task2()`, altså **modfase**.

**Dette matcher opgaven korrekt:** trykket = i takt, sluppet = modfase — modsat rækkefølge af hvad 20-points-versionen forsøgte, men nu med begge tilstande implementeret.

**Hvorfor "kun" 25 og ikke 30+ point (sandsynlige mindre fradrag):**
- `led = p1, p0` er en **ubrugt variabel** (en tuple, der aldrig refereres til igen). Det er ikke en fejl i sig selv, men "død kode", som en censor kan bemærke og trække lidt fra for.
- Samme svaghed som før: `sleep()`-kaldene blokerer, så knappen kun tjekkes ved starten af hver `task3()`-kørsel (hvert 1 sekund i "i takt"-tilstanden, hvert 1 sekund i modfase-tilstanden). Det er ikke en fejl ift. opgaveteksten, men en reaktionstid, en censor kan spørge ind til.
- Funktionsnavngivningen (`task2`, `task3`) er ikke beskrivende (`modfase()`, `i_takt()` ville være bedre stil) — kan give mindre stilistiske fradrag.

---

## 3. Sammenligning: 20 vs. 25 point (samme knap-idé, forskellig kvalitet)

| | 20-point version | 25-point version |
|---|---|---|
| Har knap | Ja | Ja |
| "I takt"-tilstand implementeret | **Nej** | Ja (begge on/off samtidig) |
| Modfase-tilstand implementeret | Ja (men uden `else`) | Ja (som `task2()`) |
| Reagerer når knap er sluppet | Nej (intet sker) | Ja (kører modfase) |
| Kodestruktur | Ren `if`, ingen `else` | Opdelt i funktioner (`task2`, `task3`) |
| Ubrugt kode | Nej | `led = p1, p0` (ubrugt) |

**Konklusion:** Forskellen på 5 ekstra point ligger primært i, at 25-points-versionen rent faktisk implementerer **begge** krævede tilstande (i takt OG modfase) og kobler dem korrekt til knappens tilstand — ikke kun én tilstand styret af knappen.

---

## 4. De to nye 30-points-forsøg (PWM-baserede)

Disse to filer ser ud til at være besvarelser af en **udvidet/anden opgave** (30 point), hvor lysstyrke (PWM/dæmpning) og brugerinput indgår — ikke kun simpel modfase. Den ene er en rettet/fuld løsning, den anden er den **originale eksamensbesvarelse, der kun gav 15 ud af 30 point**. At sammenligne dem er meget lærerigt, fordi det viser præcis, hvilke fejl der koster point.

### 4.1 — `fixed_30_points_pwm.py` (fuld, korrigeret løsning)

```python
from machine import Pin, PWM
from time import sleep

led_pwm1 = PWM(Pin(0))   # red
led_pwm2 = PWM(Pin(1))   # yellow

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
led_pwm1.freq(PWM_CARRIER)
led_pwm2.freq(PWM_CARRIER)


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


frequency = get_int("Blink frequency (0-20 Hz, 0 = no blinking): ", 0, 20)
brightness_pct = get_int("Brightness (0-100%): ", 0, 100)

duty = int(brightness_pct / 100 * 65535)


def set_leds(on):
    d = duty if on else 0
    led_pwm1.duty_u16(d)
    led_pwm2.duty_u16(d)


try:
    if frequency == 0:
        set_leds(True)          # solid, at whatever brightness was chosen (0% = off)
        while True:
            sleep(1)
    else:
        half_period = (1 / frequency) / 2
        while True:
            set_leds(True)
            sleep(half_period)
            set_leds(False)
            sleep(half_period)
except KeyboardInterrupt:
    led_pwm1.duty_u16(0)
    led_pwm2.duty_u16(0)
    led_pwm1.deinit()
    led_pwm2.deinit()
    print("Stopped, PWM deinitialized.")
```

**Hvad den gør, trin for trin:**

1. **To separate frekvens-begreber holdes adskilt** — meget vigtig pointe: `PWM_CARRIER = 1000` Hz er PWM'ens *interne* skiftefrekvens (bruges kun til at opnå en stabil dæmpning/lysstyrke, og skal være høj nok til, at øjet ikke ser flimmer). Den frekvens, brugeren indtaster (0–20 Hz), er derimod **blinke-frekvensen** — hvor tit LED'en tænder/slukker som helhed. De to blandes ikke sammen, i modsætning til i 4.2-filen (se nedenfor).
2. **`get_int()`** er en genbrugelig hjælpefunktion, der validerer brugerinput: den fanger `ValueError` (hvis brugeren taster bogstaver) og tjekker, at tallet er inden for det tilladte interval — og bliver ved med at spørge, indtil et gyldigt tal er indtastet.
3. **`duty`** beregnes korrekt ud fra den ønskede lysstyrke i procent: `brightness_pct / 100 * 65535` (65535 = maksimal 16-bit duty-værdi).
4. **`set_leds(on)`** er en ren, genbrugelig funktion: sætter begge LED'er til enten `duty` (tændt) eller `0` (slukket) — **samtidig**, altså "i takt"-dæmpning/blink.
5. **Specialtilfælde `frequency == 0`:** LED'erne lyser konstant (solidt) ved den valgte lysstyrke i stedet for at forsøge en division med 0 (`1/0` ville ellers give en `ZeroDivisionError`).
6. **`half_period = (1/frequency)/2`:** beregner korrekt, hvor længe LED'erne skal være tændt/slukket for at opnå den ønskede blink-frekvens (fuld periode = tændt + slukket).
7. **`try/except KeyboardInterrupt`:** Sikrer, at når brugeren stopper programmet (fx Ctrl+C), slukkes LED'erne pænt, og PWM-objekterne frigøres korrekt med `.deinit()` — god praksis, der undgår at pins "hænger fast" i en tilstand.

**Hvorfor denne version formentlig gav fuld pointsum (30):** Den har korrekt inputvalidering, korrekt skelnen mellem PWM-bærefrekvens og blink-frekvens, håndterer kant-tilfælde (0 Hz), og rydder pænt op ved afbrydelse. Koden er desuden opdelt i små, navngivne funktioner (god stil).

**Vigtigt at bemærke:** Denne opgave handler ikke om modfase — begge LED'er tændes og slukkes **samtidig** (`set_leds(True)` styrer begge ens). Det er altså en **"i takt"**-opgave kombineret med brugerstyret lysstyrke og frekvens, ikke en modfase-opgave. Hvis den oprindelige opgavetekst faktisk krævede modfase her, ville denne løsning mangle den del — men ud fra filnavnet ("fixed_30_points") ser det ud til, at opgaven i dette tilfælde specifikt handlede om PWM-styret blink/dæmpning, ikke modfase.

---

### 4.2 — `incomplete_30_points_worth_15points.py` (den faktiske eksamensbesvarelse, kun 15/30 point)

```python
#this gave 15 points at the exam!
from machine import Pin, PWM
from time import sleep

#this program gave 15 points doing the exam 

#button1 = Pin(6, Pin.IN, Pin.PULL_UP)

led = Pin(0, Pin.OUT)

p1 = machine.Pin(0)  #red
led_pwm1 = PWM(p1)

p0 = machine.Pin(1) #yellow
led_pwm2 = PWM(p0)

duty_step = int(input("type a brightness of PMW between 0 to 100%: "))
#duty_step = 129  


# Set PWM frequency
freqlim = 20
frequency = int(input("type a frequency between 0 to 20Hz: "))
led_pwm1.freq(frequency)
led_pwm2.freq(frequency)

try:
    while True:

        for duty_cycle in range(0, 65536, duty_step): #65536
            led_pwm1.duty_u16(duty_cycle)
            sleep(0.005)
            
            led_pwm2.duty_u16(duty_cycle)
            sleep(0.005)

        for duty_cycle in range(65536, 0, -duty_step):
            led_pwm1.duty_u16(duty_cycle)
            sleep(0.005)
            
            led_pwm2.duty_u16(duty_cycle)
            sleep(0.005)
            

except KeyboardInterrupt:
    print("Keyboard interrupt")
    led_pwm1.duty_u16(0)
    led_pwm2.duty_u16(0)

    print(led_pwm1)
    print(led_pwm2)
    led_pwm1.deinit()
    led_pwm2.deinit()
```

Her er en **fejl-for-fejl gennemgang** af, hvorfor denne kun scorede 15 ud af 30 point:

**🔴 Kritisk fejl 1 — programmet crasher før det overhovedet kører:**
```python
p1 = machine.Pin(0)
```
Øverst er kun `Pin` og `PWM` importeret fra `machine`-modulet (`from machine import Pin, PWM`) — **ikke** selve `machine`-modulet. Derfor findes navnet `machine` slet ikke i programmet, og denne linje vil give:
```
NameError: name 'machine' is not defined
```
**Rettelse:** Skriv blot `p1 = Pin(0)` (da `Pin` allerede er importeret direkte), eller tilføj `import machine` øverst, hvis man vil blive ved med at skrive `machine.Pin(...)`.

**🟠 Fejl 2 — ubrugt og modstridende pin-oprettelse:**
```python
led = Pin(0, Pin.OUT)
```
Denne linje opretter endnu et objekt på **samme fysiske pin (0)** som `p1`/`led_pwm1` bruger — men som en almindelig digital output-pin, ikke PWM. `led` bruges aldrig igen i programmet. Ud over at være død kode, kan det skabe konflikt, fordi to forskellige objekter (`led` og `led_pwm1`) begge "ejer" pin 0.
**Rettelse:** Slet linjen helt.

**🟠 Fejl 3 — begrebsforvirring: "brightness" bruges som "step-størrelse", ikke som duty-procent:**
```python
duty_step = int(input("type a brightness of PMW between 0 to 100%: "))
...
for duty_cycle in range(0, 65536, duty_step):
```
Brugeren bliver bedt om at indtaste en **lysstyrke i procent (0–100)**, men tallet bliver derefter brugt direkte som **step-størrelsen** i en `range(0, 65536, duty_step)`-løkke. Det er to helt forskellige ting:
- Hvis brugeren fx taster `50` (forventer "50 % lysstyrke"), bliver resultatet i stedet en løkke, der tæller fra 0 til 65535 i spring af 50 — dvs. en *fuld* fade fra helt slukket til helt tændt, ikke en fast lysstyrke på 50 %.
- Der er **ingen faktisk mulighed for at vælge en fast lysstyrke** — programmet laver altid en fuld "fade in/fade out"-cyklus, uanset hvad brugeren taster.
**Rettelse:** Skil de to begreber ad, som i den rettede fil: beregn en egentlig `duty`-værdi ud fra brightness-procenten (`duty = int(brightness_pct/100*65535)`), og brug en fast, uafhængig step-størrelse til selve fade-animationen, hvis en fade-effekt er ønsket.

**🟠 Fejl 4 — ingen inputvalidering:**
- Hvis brugeren taster noget, der ikke er et helt tal (fx "abc"), crasher programmet med en `ValueError` — der er intet `try/except` omkring `input()`-kaldene.
- Hvis `duty_step` bliver `0` (fx hvis brugeren taster `0`), vil `range(0, 65536, 0)` give en `ValueError: range() arg 3 must not be zero`.
- `freqlim = 20` bliver defineret, men **aldrig brugt** til rent faktisk at tjekke, om `frequency` er inden for 0–20 — variablen er ren pynt uden funktion.

**🟠 Fejl 5 — sammenblanding af PWM-bærefrekvens og blink-frekvens:**
```python
frequency = int(input("type a frequency between 0 to 20Hz: "))
led_pwm1.freq(frequency)
```
Her sættes selve **PWM-signalets frekvens** (`.freq()`) direkte til brugerens tal mellem 0–20 Hz. Men PWM-frekvensen er normalt noget, der bør ligge højt (typisk 1000+ Hz), for at dæmpningen opleves jævn og flimmerfri for øjet — 0–20 Hz er alt for lavt til en PWM-bærefrekvens og vil give en synligt flimrende/summende diode, ikke en jævn dæmpning. Derudover: **hvis brugeren taster 0**, vil `led_pwm1.freq(0)` højst sandsynligt give en runtime-fejl, fordi 0 Hz ikke er en gyldig PWM-frekvens.
Det, opgaven formentlig ønskede, var at bruge de 0–20 Hz som en **separat blinke-frekvens** (ligesom i den rettede fil, hvor `half_period` beregnes ud fra `frequency`, og selve PWM'en kører på en fast, høj bærefrekvens) — ikke at overskrive selve PWM-hardwarens frekvens.

**🟡 Fejl 6 — LED'erne er ikke rigtigt synkrone ("i takt"):**
```python
led_pwm1.duty_u16(duty_cycle)
sleep(0.005)

led_pwm2.duty_u16(duty_cycle)
sleep(0.005)
```
De to LED'er opdateres **efter hinanden** med en 5 ms forsinkelse imellem, i stedet for samtidig. Med kun 5 ms er forskellen næppe synlig for øjet, men det er teknisk ikke ægte "i takt" (synkront) — og fordoblet ventetid (10 ms i alt pr. trin) gør hele fade-cyklussen dobbelt så langsom, end den behøvede at være.

**Opsummering — hvorfor 15 ud af 30 point:**

| Problem | Alvorlighed | Konsekvens |
|---|---|---|
| `machine.Pin` uden `import machine` | 🔴 Kritisk | Programmet crasher med det samme (`NameError`) |
| `led = Pin(0, Pin.OUT)` ubrugt/i konflikt | 🟠 Middel | Død og forvirrende kode, pin-konflikt |
| "Brightness" bruges som step, ikke som duty | 🟠 Middel | Funktionen matcher ikke det, brugeren bliver bedt om |
| Ingen inputvalidering | 🟠 Middel | Programmet crasher ved forkert/edge-case input |
| PWM-frekvens forvekslet med blink-frekvens | 🟠 Middel | Forkert/flimrende output, mulig crash ved 0 Hz |
| LED'er opdateres asynkront (5 ms mellemrum) | 🟡 Lav | Lille, men reel afvigelse fra "i takt" |

Trods fejlene viser koden dog: korrekt brug af `PWM`, `duty_u16()`, `try/except KeyboardInterrupt` med oprydning (`deinit()`), og en fungerende (om end fejlfortolket) fade-løkke — hvilket forklarer, at den stadig fik halvdelen af pointene (15/30) for delvist korrekt PWM-forståelse, selvom kernefunktionaliteten (bruger-styret lysstyrke + frekvens) ikke virkede som tiltænkt.

---

## 5. Samlet pointoversigt

| Fil | Point | Knap | I takt | Modfase | Brugerinput | PWM | Største svaghed |
|---|---|---|---|---|---|---|---|
| 10-point (reeksamen) | 10/? | Nej | Nej | Ja | Nej | Nej | Ingen knap-styring overhovedet |
| 20-point (1. eksamen) | 20/? | Ja | **Nej** | Delvist | Nej | Nej | Mangler "i takt" og `else`-gren |
| 25-point (reeksamen) | 25/? | Ja | Ja | Ja | Nej | Nej | Ubrugt variabel, blokerende `sleep()` |
| `incomplete_…15points` | 15/30 | Nej | Delvist (5 ms lag) | N/A | Ja (u. validering) | Ja | `NameError`-crash + logikfejl i brightness/frekvens |
| `fixed_30_points_pwm` | 30/30 | Nej | Ja (fuldt synkront) | N/A | Ja (m. validering) | Ja | Ingen — komplet, robust løsning |

---

## 6. Tjekliste — undgå disse fejl til din egen eksamen

1. **Importér det, du bruger.** Hvis du skriver `machine.Pin(...)`, skal du enten `import machine` eller kun bruge `Pin(...)` direkte efter `from machine import Pin`.
2. **Slet ubrugt/gammel kode** (fx overflødige `led = Pin(...)`-linjer eller ubrugte variabler som `led = p1, p0`) — det ser rodet ud og kan forvirre censor.
3. **Match variabelnavne til deres faktiske brug.** Hvis noget hedder `brightness` eller `duty_step`, skal det rent faktisk bruges som det, navnet lover — ikke genbruges til noget andet (fx en løkke-step-størrelse).
4. **Adskil PWM-bærefrekvens fra blink-frekvens**, hvis opgaven beder om begge dele: brug en fast, høj bærefrekvens (`.freq(1000)`) til selve dæmpningen, og beregn selv, hvor længe LED'en skal være tændt/slukket for at opnå den ønskede blinke-frekvens.
5. **Valider altid brugerinput** med `try/except ValueError` og tjek af, at tallet er inden for det tilladte interval — ellers crasher programmet ved uventet input.
6. **Håndtér kant-tilfælde** (fx frekvens = 0, eller step = 0) eksplicit, i stedet for at lade Python smide en fejl.
7. **Implementér ALLE krævede tilstande fra opgaveteksten** — hvis opgaven beder om både "i takt" OG "modfase" via en knap, skal begge grene (`if`/`else`) rent faktisk implementere hver sin tilstand, ikke kun én styret af knappen.
8. **Ryd pænt op ved afslutning** (`deinit()` på PWM-objekter, sluk LED'er) i et `try/except KeyboardInterrupt` — det viser god programmeringspraksis og undgår at pins "hænger" i en tilstand.
9. **Brug hjælpefunktioner** (som `get_int()` og `set_leds()` i den rettede fil) til at gøre koden mere læsbar og undgå gentagelser — det scorer typisk bedre stilmæssigt end lange, ukommenterede blokke.
