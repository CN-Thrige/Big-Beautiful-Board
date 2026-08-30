# Ohms lov i serie- og parallelforbindelser

En pædagogisk gennemgang med eksempler og udregninger.

---

## 1. Grundlaget: Ohms lov

Ohms lov beskriver sammenhængen mellem **spænding (U)**, **strøm (I)** og **modstand (R)** i en elektrisk kreds:

$$
U = I \cdot R
$$

Hvor:
- **U** = spænding, målt i volt (V)
- **I** = strømstyrke, målt i ampere (A)
- **R** = modstand, målt i ohm (Ω)

Formlen kan omskrives, alt efter hvad du skal finde:

$$
I = \frac{U}{R} \qquad \text{og} \qquad R = \frac{U}{I}
$$

**Huskeregel (trekant-metoden):**

```
      U
    -----
   I  |  R
```

Dæk den størrelse til, du søger — de to andre viser dig, om de skal ganges eller divideres. Eksempel: dækker du **U** til, står **I** og **R** tilbage side om side, hvilket betyder "gang dem sammen" ($U = I \cdot R$). Dækker du **I** til, står **U** over **R**, hvilket betyder "divider" ($I = U/R$).

### Hvorfor hænger de tre størrelser sammen?

Tænk på strøm som vand, der løber gennem et rør:

- **Spænding (U)** er "trykket", der presser vandet/strømmen gennem kredsen — jo højere spænding, jo kraftigere skub.
- **Modstand (R)** er, hvor snævert røret er — jo smallere rør (højere modstand), jo sværere er det for vandet at komme igennem.
- **Strøm (I)** er, hvor meget vand der faktisk løber igennem pr. sekund — resultatet af trykket og rørets bredde.

Med et fast tryk (spænding) giver et smallere rør (højere modstand) mindre gennemstrømning (lavere strøm). Det er præcis, hvad $I = U/R$ siger: strømmen falder, når modstanden stiger.

---

## 2. Serieforbindelse

I en **serieforbindelse** sidder komponenterne efter hinanden i én sammenhængende "løkke". Strømmen har kun én vej at løbe.

### Karakteristika ved serieforbindelse

| Størrelse | Regel |
|---|---|
| Strøm (I) | **Samme** strøm overalt i kredsen: $I_{tot} = I_1 = I_2 = I_3$ |
| Spænding (U) | Fordeles over komponenterne: $U_{tot} = U_1 + U_2 + U_3$ |
| Modstand (R) | Modstandene lægges sammen: $R_{tot} = R_1 + R_2 + R_3$ |

**Hvorfor?** Tænk på det som en enkelt vej — al strøm skal igennem hver eneste modstand, så strømmen kan ikke "vælge" en anden rute. Til gengæld skal spændingskilden "presse" strømmen igennem alle modstandene efter hinanden, så den samlede modstand vokser, og spændingen deles mellem dem.

### Eksempel: Serieforbindelse

Du har et 12V batteri koblet til to modstande i serie:
- $R_1 = 4\,\Omega$
- $R_2 = 8\,\Omega$

**Trin 1: Find den samlede modstand**

$$
R_{tot} = R_1 + R_2 = 4\,\Omega + 8\,\Omega = 12\,\Omega
$$

**Trin 2: Find den samlede strøm**

$$
I_{tot} = \frac{U_{tot}}{R_{tot}} = \frac{12\,V}{12\,\Omega} = 1\,A
$$

**Trin 3: Find spændingsfaldet over hver modstand**

Da strømmen er den samme overalt (1 A), kan vi bruge Ohms lov på hver modstand for sig:

$$
U_1 = I \cdot R_1 = 1\,A \cdot 4\,\Omega = 4\,V
$$

$$
U_2 = I \cdot R_2 = 1\,A \cdot 8\,\Omega = 8\,V
$$

**Kontrol:** $U_1 + U_2 = 4\,V + 8\,V = 12\,V$ ✅ — det stemmer med batteriets spænding.

### Eksempel 2: Serieforbindelse med tre modstande

Nu prøver vi med tre modstande i serie og et 24V batteri:
- $R_1 = 2\,\Omega$
- $R_2 = 6\,\Omega$
- $R_3 = 4\,\Omega$

**Trin 1: Læg modstandene sammen**

$$
R_{tot} = R_1 + R_2 + R_3 = 2\,\Omega + 6\,\Omega + 4\,\Omega = 12\,\Omega
$$

**Trin 2: Find den fælles strøm**

Fordi det er en serieforbindelse, er der kun én vej for strømmen — så vi regner strømmen ud fra hele kredsen på én gang:

$$
I_{tot} = \frac{U_{tot}}{R_{tot}} = \frac{24\,V}{12\,\Omega} = 2\,A
$$

**Trin 3: Find spændingsfaldet over hver enkelt modstand**

Samme strøm (2 A) løber gennem alle tre, så vi genbruger $U = I \cdot R$ tre gange:

$$
U_1 = I \cdot R_1 = 2\,A \cdot 2\,\Omega = 4\,V
$$

$$
U_2 = I \cdot R_2 = 2\,A \cdot 6\,\Omega = 12\,V
$$

$$
U_3 = I \cdot R_3 = 2\,A \cdot 4\,\Omega = 8\,V
$$

**Trin 4: Kontrollér resultatet**

Spændingsfaldene skal give batteriets spænding tilbage, når de lægges sammen:

$$
U_1 + U_2 + U_3 = 4\,V + 12\,V + 8\,V = 24\,V \; ✅
$$

**Læringspointe:** Læg mærke til, at den modstand med højst værdi ($R_2 = 6\,\Omega$) også får det største spændingsfald (12 V). Det giver mening — jo mere "modstand" en komponent yder, jo mere spænding skal "bruges" på at presse strømmen igennem netop den komponent. Man siger, at spændingen fordeler sig **proportionalt** med modstanden i en serieforbindelse.

---

## 3. Parallelforbindelse

I en **parallelforbindelse** sidder komponenterne side om side, hver på sin egen "gren". Strømmen kan vælge mellem flere veje.

### Karakteristika ved parallelforbindelse

| Størrelse | Regel |
|---|---|
| Spænding (U) | **Samme** spænding over hver gren: $U_{tot} = U_1 = U_2 = U_3$ |
| Strøm (I) | Fordeles mellem grenene: $I_{tot} = I_1 + I_2 + I_3$ |
| Modstand (R) | Reciprok-sum: $\dfrac{1}{R_{tot}} = \dfrac{1}{R_1} + \dfrac{1}{R_2} + \dfrac{1}{R_3}$ |

**Hvorfor?** Alle grenene er koblet til de samme to punkter, så de "føler" den samme spænding. Men da der nu er flere veje for strømmen at løbe, bliver den samlede modstand faktisk **mindre** end den mindste enkeltmodstand — jo flere veje, jo lettere er det for strømmen at komme igennem.

### Eksempel: Parallelforbindelse

Samme to modstande, men nu koblet parallelt til et 12V batteri:
- $R_1 = 4\,\Omega$
- $R_2 = 8\,\Omega$

**Trin 1: Find den samlede modstand**

$$
\frac{1}{R_{tot}} = \frac{1}{R_1} + \frac{1}{R_2} = \frac{1}{4} + \frac{1}{8} = \frac{2}{8} + \frac{1}{8} = \frac{3}{8}
$$

$$
R_{tot} = \frac{8}{3} \approx 2{,}67\,\Omega
$$

*(Bemærk: $2{,}67\,\Omega$ er mindre end den mindste modstand på $4\,\Omega$ — det giver mening, da strømmen nu har to veje at løbe.)*

**Trin 2: Find strømmen i hver gren**

Da spændingen er den samme over begge modstande (12 V), regner vi hver gren for sig:

$$
I_1 = \frac{U}{R_1} = \frac{12\,V}{4\,\Omega} = 3\,A
$$

$$
I_2 = \frac{U}{R_2} = \frac{12\,V}{8\,\Omega} = 1{,}5\,A
$$

**Trin 3: Find den samlede strøm**

$$
I_{tot} = I_1 + I_2 = 3\,A + 1{,}5\,A = 4{,}5\,A
$$

**Kontrol med Ohms lov på hele kredsen:**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{12\,V}{2{,}67\,\Omega} \approx 4{,}5\,A \; ✅
$$

### Eksempel 2: Parallelforbindelse med tre modstande

Tre modstande koblet parallelt til et 6V batteri:
- $R_1 = 10\,\Omega$
- $R_2 = 5\,\Omega$
- $R_3 = 20\,\Omega$

**Trin 1: Opstil reciprok-summen**

$$
\frac{1}{R_{tot}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} = \frac{1}{10} + \frac{1}{5} + \frac{1}{20}
$$

**Trin 2: Find fælles nævner og læg brøkerne sammen**

Fælles nævner for 10, 5 og 20 er 20:

$$
\frac{1}{10} = \frac{2}{20}, \qquad \frac{1}{5} = \frac{4}{20}, \qquad \frac{1}{20} = \frac{1}{20}
$$

$$
\frac{1}{R_{tot}} = \frac{2}{20} + \frac{4}{20} + \frac{1}{20} = \frac{7}{20}
$$

**Trin 3: "Vend brøken om" for at finde $R_{tot}$**

$$
R_{tot} = \frac{20}{7} \approx 2{,}86\,\Omega
$$

*(Igen: mindre end den mindste enkeltmodstand på $5\,\Omega$ — helt som forventet med tre parallelle veje.)*

**Trin 4: Find strømmen i hver gren**

Alle tre grene "ser" den samme spænding (6 V), så vi regner hver for sig med Ohms lov:

$$
I_1 = \frac{U}{R_1} = \frac{6\,V}{10\,\Omega} = 0{,}6\,A
$$

$$
I_2 = \frac{U}{R_2} = \frac{6\,V}{5\,\Omega} = 1{,}2\,A
$$

$$
I_3 = \frac{U}{R_3} = \frac{6\,V}{20\,\Omega} = 0{,}3\,A
$$

**Trin 5: Læg strømmene sammen for at finde den samlede strøm**

$$
I_{tot} = I_1 + I_2 + I_3 = 0{,}6\,A + 1{,}2\,A + 0{,}3\,A = 2{,}1\,A
$$

**Trin 6: Kontrollér med Ohms lov på hele kredsen**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{6\,V}{2{,}86\,\Omega} \approx 2{,}1\,A \; ✅
$$

**Læringspointe:** Læg mærke til, at $R_2 = 5\,\Omega$ (den mindste modstand) trækker den største strøm (1,2 A). Det giver mening — jo mindre modstand en gren har, jo "lettere" er det for strømmen at løbe netop den vej, så den tiltrækker sig en større andel af den samlede strøm.

---

## 4. Genvej for to modstande parallelt

Når der kun er **to** modstande parallelt, kan du bruge en hurtigere formel i stedet for reciprok-summen:

$$
R_{tot} = \frac{R_1 \cdot R_2}{R_1 + R_2}
$$

Tjek med eksemplet ovenfor:

$$
R_{tot} = \frac{4 \cdot 8}{4 + 8} = \frac{32}{12} \approx 2{,}67\,\Omega
$$

Samme resultat som før — men hurtigere at regne, når I kun er to modstande.

---

## 5. Blandet kredsløb (serie + parallel kombineret)

I virkeligheden er kredsløb ofte en blanding af serie- og parallelforbindelser. Tricket er at **arbejde sig indefra og ud**: find først den samlede modstand af den parallelle del, og regn derefter resten som en almindelig serieforbindelse.

### Eksempel: Blandet kredsløb

Et 20V batteri er koblet til $R_1$ i serie med en parallelkobling af $R_2$ og $R_3$:
- $R_1 = 2\,\Omega$ (i serie)
- $R_2 = 6\,\Omega$ og $R_3 = 3\,\Omega$ (parallelt med hinanden)

```
        R1 (serie)
  ─────/\/\/\─────┬─────┐
                  │     │
                 R2     R3   (parallelt)
                  │     │
  ────────────────┴─────┘
```

**Trin 1: Regn den parallelle del sammen først**

$R_2$ og $R_3$ sidder parallelt, så vi bruger genvejsformlen for to modstande:

$$
R_{23} = \frac{R_2 \cdot R_3}{R_2 + R_3} = \frac{6 \cdot 3}{6+3} = \frac{18}{9} = 2\,\Omega
$$

**Trin 2: Læg den parallelle "blok" i serie med $R_1$**

Nu kan vi behandle $R_{23}$ som én almindelig modstand, der sidder i serie med $R_1$:

$$
R_{tot} = R_1 + R_{23} = 2\,\Omega + 2\,\Omega = 4\,\Omega
$$

**Trin 3: Find den samlede strøm fra batteriet**

$$
I_{tot} = \frac{U_{tot}}{R_{tot}} = \frac{20\,V}{4\,\Omega} = 5\,A
$$

Denne strøm (5 A) er den, der løber gennem $R_1$, fordi $R_1$ sidder alene i serie med resten.

**Trin 4: Find spændingen over $R_1$ og over den parallelle blok**

$$
U_1 = I_{tot} \cdot R_1 = 5\,A \cdot 2\,\Omega = 10\,V
$$

$$
U_{23} = I_{tot} \cdot R_{23} = 5\,A \cdot 2\,\Omega = 10\,V
$$

**Kontrol:** $U_1 + U_{23} = 10\,V + 10\,V = 20\,V$ ✅

**Trin 5: Find strømmen i hver af de to parallelle grene**

$U_{23} = 10\,V$ er den spænding, som *begge* $R_2$ og $R_3$ "ser", fordi de sidder parallelt med hinanden:

$$
I_2 = \frac{U_{23}}{R_2} = \frac{10\,V}{6\,\Omega} \approx 1{,}67\,A
$$

$$
I_3 = \frac{U_{23}}{R_3} = \frac{10\,V}{3\,\Omega} \approx 3{,}33\,A
$$

**Kontrol:** $I_2 + I_3 = 1{,}67\,A + 3{,}33\,A = 5\,A = I_{tot}$ ✅ — strømmen fra batteriet fordeler sig præcis mellem de to grene og samles igen.

**Læringspointe:** Metoden er altid den samme for blandede kredsløb: **forenkl trin for trin**. Find en gruppe modstande, der er rent parallel eller rent serie, regn den sammen til én "erstatningsmodstand", og gentag, indtil hele kredsløbet er reduceret til én eneste modstand.

---

## 6. Sammenligning: Serie vs. Parallel

| | Serieforbindelse | Parallelforbindelse |
|---|---|---|
| **Strøm** | Ens overalt | Fordeles mellem grene |
| **Spænding** | Fordeles over komponenter | Ens over alle grene |
| **Samlet modstand** | Vokser: $R_{tot} = R_1+R_2+\dots$ | Falder: $\dfrac{1}{R_{tot}}=\dfrac{1}{R_1}+\dfrac{1}{R_2}+\dots$ |
| **Analogi** | Én lang vej — alle skal samme sted igennem | Flere parallelle veje — trafikken deler sig |
| **Hvis én komponent fejler** | Hele kredsen afbrydes | De andre grene virker stadig |

---

## 7. Hverdagseksempel

**Julelys (gammeldags serie):** Hvis lyskæden er koblet i serie, og én pære springer, går hele kæden ud — strømmen har jo ingen anden vej at løbe.

**Stikkontakter i et hjem (parallel):** Dine stikkontakter er koblet parallelt. Derfor kan du slukke for lampen i stuen, uden at fjernsynet i soveværelset også slukker — hver "gren" fungerer uafhængigt, og de har alle samme spænding (fx 230 V).

**Sikringer i en gruppetavle (parallel):** Grunden til, at dit hjem er delt op i flere "grupper" (fx en til køkken, en til stuen), er netop, at de er koblet parallelt med hinanden ud fra samme spændingskilde. Går sikringen på køkkengruppen, mister du kun strømmen dér — ikke i resten af huset.

**Batterier i en fjernbetjening (serie):** To AA-batterier på 1,5 V hver, sat i serie inde i en fjernbetjening, giver tilsammen 3 V — fordi spændingerne lægges sammen i en serieforbindelse, ligesom $U_1+U_2$ i eksempel 1.

---

## 8. Øvelsesopgave (prøv selv!)

To modstande, $R_1 = 6\,\Omega$ og $R_2 = 3\,\Omega$, kobles til en 9V spændingskilde.

**a)** Beregn den samlede modstand, strøm og spænding over hver modstand, hvis de kobles i **serie**.

**b)** Beregn det samme, hvis de kobles **parallelt**.

<details>
<summary>Klik for facit</summary>

**a) Serie:**
- $R_{tot} = 6 + 3 = 9\,\Omega$
- $I_{tot} = 9V / 9\Omega = 1\,A$
- $U_1 = 1 \cdot 6 = 6\,V$, $U_2 = 1 \cdot 3 = 3\,V$

**b) Parallel:**
- $R_{tot} = \dfrac{6 \cdot 3}{6+3} = \dfrac{18}{9} = 2\,\Omega$
- $U_1 = U_2 = 9\,V$ (samme som kilden)
- $I_1 = 9/6 = 1{,}5\,A$, $I_2 = 9/3 = 3\,A$
- $I_{tot} = 1{,}5 + 3 = 4{,}5\,A$

</details>
