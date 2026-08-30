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

Dæk den størrelse til, du søger — de to andre viser dig, om de skal ganges eller divideres.

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

## 5. Sammenligning: Serie vs. Parallel

| | Serieforbindelse | Parallelforbindelse |
|---|---|---|
| **Strøm** | Ens overalt | Fordeles mellem grene |
| **Spænding** | Fordeles over komponenter | Ens over alle grene |
| **Samlet modstand** | Vokser: $R_{tot} = R_1+R_2+\dots$ | Falder: $\dfrac{1}{R_{tot}}=\dfrac{1}{R_1}+\dfrac{1}{R_2}+\dots$ |
| **Analogi** | Én lang vej — alle skal samme sted igennem | Flere parallelle veje — trafikken deler sig |
| **Hvis én komponent fejler** | Hele kredsen afbrydes | De andre grene virker stadig |

---

## 6. Hverdagseksempel

**Julelys (gammeldags serie):** Hvis lyskæden er koblet i serie, og én pære springer, går hele kæden ud — strømmen har jo ingen anden vej at løbe.

**Stikkontakter i et hjem (parallel):** Dine stikkontakter er koblet parallelt. Derfor kan du slukke for lampen i stuen, uden at fjernsynet i soveværelset også slukker — hver "gren" fungerer uafhængigt, og de har alle samme spænding (fx 230 V).

---

## 7. Øvelsesopgave (prøv selv!)

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
