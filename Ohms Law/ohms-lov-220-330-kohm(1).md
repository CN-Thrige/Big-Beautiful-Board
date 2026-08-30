# Ohms lov med praktiske modstandsværdier (220 Ω, 330 Ω og kΩ)

## 1. Ohms lov — grundformlen

$$
U = I \cdot R \qquad I = \frac{U}{R} \qquad R = \frac{U}{I}
$$

- **U** = spænding i volt (V)
- **I** = strøm i ampere (A)
- **R** = modstand i ohm (Ω)

---

## 2. Om enheder: Ω, kΩ og mA

I elektronik er 220 Ω og 330 Ω blandt de allermest almindelige modstandsværdier — du finder dem i stort set enhver komponentkasse. Når modstande bliver større, skriver man dem ofte i **kilo-ohm (kΩ)** i stedet for at skrive mange nuller:

$$
1\,k\Omega = 1000\,\Omega
$$

Eksempel: $2{,}2\,k\Omega = 2200\,\Omega$

Tilsvarende bliver strømmen ofte meget lille (under 1 A), så den angives i **milliampere (mA)**:

$$
1\,A = 1000\,mA \qquad \Rightarrow \qquad 1\,mA = 0{,}001\,A
$$

**Praktisk tommelfingerregel:** Hvis du ganger V med kΩ, får du strømmen direkte i mA:

$$
I(mA) = \frac{U(V)}{R(k\Omega)}
$$

---

## 3. Eksempel 1: To modstande i serie (220 Ω og 330 Ω)

Et 12V batteri koblet til $R_1 = 220\,\Omega$ og $R_2 = 330\,\Omega$ i serie.

**Samlet modstand:**

$$
R_{tot} = R_1 + R_2 = 220\,\Omega + 330\,\Omega = 550\,\Omega = 0{,}55\,k\Omega
$$

**Strøm (samme overalt i en serieforbindelse):**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{12\,V}{550\,\Omega} \approx 0{,}0218\,A = 21{,}8\,mA
$$

**Spænding over hver modstand:**

$$
U_1 = I \cdot R_1 = 0{,}0218\,A \cdot 220\,\Omega \approx 4{,}8\,V
$$

$$
U_2 = I \cdot R_2 = 0{,}0218\,A \cdot 330\,\Omega \approx 7{,}2\,V
$$

**Kontrol:** $4{,}8\,V + 7{,}2\,V = 12{,}0\,V$ ✅

---

## 4. Eksempel 2: To modstande parallelt (220 Ω og 330 Ω)

Samme to modstande, men nu parallelt til 12V.

**Samlet modstand (genvej for to modstande):**

$$
R_{tot} = \frac{R_1 \cdot R_2}{R_1+R_2} = \frac{220 \cdot 330}{220+330} = \frac{72600}{550} = 132\,\Omega
$$

**Strøm i hver gren (spændingen er ens over begge, 12 V):**

$$
I_1 = \frac{U}{R_1} = \frac{12\,V}{220\,\Omega} \approx 0{,}0545\,A = 54{,}5\,mA
$$

$$
I_2 = \frac{U}{R_2} = \frac{12\,V}{330\,\Omega} \approx 0{,}0364\,A = 36{,}4\,mA
$$

**Samlet strøm:**

$$
I_{tot} = I_1 + I_2 = 54{,}5\,mA + 36{,}4\,mA = 90{,}9\,mA
$$

**Kontrol:**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{12\,V}{132\,\Omega} \approx 90{,}9\,mA \; ✅
$$

---

## 5. Eksempel 3: Blandet kredsløb (R1=220 Ω, R2=330 Ω, R3=220 Ω parallelt, 24 V)

Dette er kredsløbet fra jeres gennemgang: $R_1 = 220\,\Omega$ i serie med en parallelkobling af $R_2 = 330\,\Omega$ og $R_3 = 220\,\Omega$, koblet til 24 V.

```
        R1 (serie, 220Ω)
  ─────/\/\/\─────┬─────┐
                  │     │
              R2 330Ω  R3 220Ω   (parallelt)
                  │     │
  ────────────────┴─────┘
```

**Trin 1 — Den parallelle del:**

$$
R_{23} = \frac{R_2 \cdot R_3}{R_2+R_3} = \frac{330 \cdot 220}{330+220} = \frac{72600}{550} = 132\,\Omega
$$

**Trin 2 — Saml med R1 i serie:**

$$
R_{tot} = R_1 + R_{23} = 220\,\Omega + 132\,\Omega = 352\,\Omega
$$

**Trin 3 — Samlet strøm fra batteriet:**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{24\,V}{352\,\Omega} \approx 0{,}0682\,A = 68{,}2\,mA
$$

**Trin 4 — Spænding over R1 og over den parallelle blok:**

$$
U_1 = I_{tot} \cdot R_1 = 0{,}0682\,A \cdot 220\,\Omega \approx 15{,}0\,V
$$

$$
U_{23} = I_{tot} \cdot R_{23} = 0{,}0682\,A \cdot 132\,\Omega \approx 9{,}0\,V
$$

**Kontrol:** $15{,}0\,V + 9{,}0\,V = 24{,}0\,V$ ✅

*Bemærk: Her bruges $R_{23} = 132\,\Omega$ — altså den parallelle blok alene — og ikke $R_{tot} = 352\,\Omega$, som er hele kredsløbets modstand.*

**Trin 5 — Strømmen i hver af de to parallelle grene ($U_{23} = 9\,V$ over begge):**

$$
I_2 = \frac{U_{23}}{R_2} = \frac{9\,V}{330\,\Omega} \approx 0{,}0273\,A = 27{,}3\,mA
$$

$$
I_3 = \frac{U_{23}}{R_3} = \frac{9\,V}{220\,\Omega} \approx 0{,}0409\,A = 40{,}9\,mA
$$

**Kontrol:** $27{,}3\,mA + 40{,}9\,mA \approx 68{,}2\,mA = I_{tot}$ ✅

---

## 6. Eksempel 4: Med en modstand i kΩ (LED-forkoblingsmodstand)

Et klassisk eksempel fra elektronik: en LED skal beskyttes med en seriemodstand. Batteri på 9V, seriemodstand $R = 2{,}2\,k\Omega$ (en meget almindelig værdi, ofte brugt sammen med 220Ω og 330Ω i kredsløb).

**Strøm gennem kredsen:**

$$
I = \frac{U}{R} = \frac{9\,V}{2{,}2\,k\Omega} \approx 4{,}09\,mA
$$

Bemærk, at fordi R stod i kΩ, kom svaret automatisk ud i mA — det er den praktiske genvej nævnt i afsnit 2.

**Hvis vi i stedet ville regne i "rene" enheder (Ω og A):**

$$
I = \frac{9\,V}{2200\,\Omega} = 0{,}00409\,A = 4{,}09\,mA
$$

Samme resultat — kΩ/mA-genvejen sparer dig bare for at skulle rykke om på decimalerne.

---

## 7. Eksempel 5: Serieforbindelse *inde i* en parallelforbindelse

Nu vender vi det om i forhold til eksempel 3: I stedet for én modstand i serie med en parallelblok, har vi to **grene**, der hver består af modstande i serie — og de to grene sidder parallelt med hinanden.

- Gren A: $R_1 = 220\,\Omega$ og $R_2 = 330\,\Omega$ i **serie**
- Gren B: $R_3 = 220\,\Omega$ alene
- Grenene A og B sidder **parallelt** med hinanden på et 24V batteri

```
  ┌──/\/\/\──/\/\/\──┐   Gren A: R1 (220Ω) + R2 (330Ω) i serie
  │    R1       R2   │
24V                  ├─ (parallel-knudepunkt)
  │                  │
  └──────/\/\/\──────┘   Gren B: R3 (220Ω) alene
            R3
```

**Trin 1 — Regn hver gren sammen for sig (serie inde i grenen):**

$$
R_A = R_1 + R_2 = 220\,\Omega + 330\,\Omega = 550\,\Omega
$$

$$
R_B = R_3 = 220\,\Omega
$$

**Trin 2 — Nu er der kun to "modstande" tilbage (grenene A og B), som sidder parallelt:**

$$
R_{tot} = \frac{R_A \cdot R_B}{R_A + R_B} = \frac{550 \cdot 220}{550+220} = \frac{121000}{770} \approx 157{,}1\,\Omega
$$

**Trin 3 — Spændingen er ens over begge grene (24 V, fordi de sidder direkte parallelt på batteriet):**

$$
U_A = U_B = 24\,V
$$

**Trin 4 — Strømmen i hver gren (Ohms lov på grenens samlede modstand):**

$$
I_A = \frac{U_A}{R_A} = \frac{24\,V}{550\,\Omega} \approx 43{,}6\,mA
$$

$$
I_B = \frac{U_B}{R_B} = \frac{24\,V}{220\,\Omega} \approx 109{,}1\,mA
$$

**Trin 5 — Den samlede strøm fra batteriet:**

$$
I_{tot} = I_A + I_B = 43{,}6\,mA + 109{,}1\,mA = 152{,}7\,mA
$$

**Kontrol:**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{24\,V}{157{,}1\,\Omega} \approx 152{,}8\,mA \; ✅ \;(\text{lille afrundingsforskel})
$$

**Trin 6 — Fordelingen inde i gren A (spændingsfald over R1 og R2):**

Fordi $R_1$ og $R_2$ sidder i serie *inde i* gren A, deles de 24 V mellem dem efter samme strøm ($I_A = 43{,}6\,mA$):

$$
U_1 = I_A \cdot R_1 = 0{,}0436\,A \cdot 220\,\Omega \approx 9{,}6\,V
$$

$$
U_2 = I_A \cdot R_2 = 0{,}0436\,A \cdot 330\,\Omega \approx 14{,}4\,V
$$

**Kontrol:** $9{,}6\,V + 14{,}4\,V = 24{,}0\,V$ ✅ — det matcher spændingen over hele gren A.

**Læringspointe:** Forskellen på eksempel 3 og 5 viser to grundtyper af blandede kredsløb:
- **Eksempel 3:** Parallel-blok sidder i serie med resten → strømmen er ens gennem seriedelen, spændingen deles.
- **Eksempel 5:** Serie-grene sidder parallelt med hinanden → spændingen er ens over hver gren, strømmen deles mellem grenene.

---

## 8. Eksempel 6: To parallelblokke i serie med hinanden

En variant, hvor to *forskellige* parallelkoblinger sidder efter hinanden i serie. Batteri på 12V.

- Blok 1: $R_1 = 220\,\Omega \parallel R_2 = 330\,\Omega$
- Blok 2: $R_3 = 220\,\Omega \parallel R_4 = 1\,k\Omega$
- Blok 1 og Blok 2 sidder i **serie** med hinanden

**Trin 1 — Regn hver parallelblok sammen for sig:**

$$
R_{blok1} = \frac{220 \cdot 330}{220+330} = \frac{72600}{550} = 132\,\Omega
$$

$$
R_{blok2} = \frac{220 \cdot 1000}{220+1000} = \frac{220000}{1220} \approx 180{,}3\,\Omega
$$

**Trin 2 — Læg de to "erstatningsmodstande" sammen i serie:**

$$
R_{tot} = R_{blok1} + R_{blok2} = 132\,\Omega + 180{,}3\,\Omega = 312{,}3\,\Omega
$$

**Trin 3 — Find den samlede strøm (den løber gennem begge blokke, da de er i serie):**

$$
I_{tot} = \frac{U}{R_{tot}} = \frac{12\,V}{312{,}3\,\Omega} \approx 38{,}4\,mA
$$

**Trin 4 — Spænding over hver blok:**

$$
U_{blok1} = I_{tot} \cdot R_{blok1} = 0{,}0384\,A \cdot 132\,\Omega \approx 5{,}1\,V
$$

$$
U_{blok2} = I_{tot} \cdot R_{blok2} = 0{,}0384\,A \cdot 180{,}3\,\Omega \approx 6{,}9\,V
$$

**Kontrol:** $5{,}1\,V + 6{,}9\,V = 12{,}0\,V$ ✅

**Trin 5 — Fordel strømmen inde i hver blok (spændingen 5,1 V hhv. 6,9 V er den, hver blok "ser"):**

I blok 1:
$$
I_1 = \frac{5{,}1\,V}{220\,\Omega} \approx 23{,}2\,mA \qquad I_2 = \frac{5{,}1\,V}{330\,\Omega} \approx 15{,}5\,mA
$$
Kontrol: $23{,}2 + 15{,}5 \approx 38{,}7\,mA \approx I_{tot}$ ✅ (lille afrunding)

I blok 2:
$$
I_3 = \frac{6{,}9\,V}{220\,\Omega} \approx 31{,}4\,mA \qquad I_4 = \frac{6{,}9\,V}{1000\,\Omega} \approx 6{,}9\,mA
$$
Kontrol: $31{,}4 + 6{,}9 \approx 38{,}3\,mA \approx I_{tot}$ ✅

**Læringspointe:** Uanset hvor kompliceret et kredsløb ser ud, virker samme opskrift altid: find den mindste "rene" serie- eller parallelgruppe, klap den sammen til én erstatningsmodstand, og gentag processen, indtil hele kredsløbet er reduceret til én modstand. Byg derefter strøm og spænding op igen "udefra og ind" — modsat den rækkefølge, du forenklede i.

---

## 9. Hurtig opsummeringstabel

| Værdi | Omregning |
|---|---|
| $220\,\Omega$ | $0{,}22\,k\Omega$ |
| $330\,\Omega$ | $0{,}33\,k\Omega$ |
| $2{,}2\,k\Omega$ | $2200\,\Omega$ |
| $1\,A$ | $1000\,mA$ |
| $68{,}2\,mA$ | $0{,}0682\,A$ |
