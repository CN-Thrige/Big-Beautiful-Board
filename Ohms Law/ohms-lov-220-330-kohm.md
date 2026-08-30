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

## 7. Hurtig opsummeringstabel

| Værdi | Omregning |
|---|---|
| $220\,\Omega$ | $0{,}22\,k\Omega$ |
| $330\,\Omega$ | $0{,}33\,k\Omega$ |
| $2{,}2\,k\Omega$ | $2200\,\Omega$ |
| $1\,A$ | $1000\,mA$ |
| $68{,}2\,mA$ | $0{,}0682\,A$ |
