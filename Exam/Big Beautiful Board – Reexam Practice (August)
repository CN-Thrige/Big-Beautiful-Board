# Big Beautiful Board – Reexam Practice (August)

Based on your actual slides: Lyskryds.pptx, Statemachine_v2.pptx, PWM.pptx,
Spændingsdeler_Pico.xlsx, plus the board photo and repo README.

## ⚠️ Pin assumptions — confirm against your own board before relying on these

Confirmed from your own working code: `GP6` = button1, `GP0` = red LED, `GP1` = yellow LED.
Everything else (button2, green LED, the second red/yellow/green group) is a placeholder —
check your board's silkscreen labels (D1–D6, U1/U2) and swap in the real GP numbers.

```
button1 = GP6
button2 = GP7        # ASSUMED
red1    = GP0        # confirmed
yellow1 = GP1         # confirmed
green1  = GP2        # ASSUMED
red2    = GP3        # ASSUMED (second traffic light group)
yellow2 = GP4        # ASSUMED
green2  = GP5        # ASSUMED
adc_pin = GP26 (ADC0) # ASSUMED, for battery-divider exercise
```

---

## 1. Single traffic light — the taught function-state pattern

Your teacher's slide 9 code (`state=state0; while state: state=state()`) is the pattern
to reproduce on the exam, just driving real LEDs instead of printing colored text.

```python
from machine import Pin
from time import sleep

red = Pin(0, Pin.OUT)
yellow = Pin(1, Pin.OUT)
green = Pin(2, Pin.OUT)

def all_off():
    red.off(); yellow.off(); green.off()

def state_green():
    all_off()
    green.on()
    print("Grøn! Kør")
    sleep(5.5)
    return state_yellow

def state_yellow():
    all_off()
    yellow.on()
    print("Gul! stop")
    sleep(1.5)
    return state_red

def state_red():
    all_off()
    red.on()
    print("Rød! stop")
    sleep(5.5)
    return state_green

state = state_green   # initial state
while state:
    state = state()
```

---

## 2. Full intersection (Lyskryds) — Nord-Syd / Øst-Vest, matches your slide 4 diagram

Your slides show the real UK 4-phase cycle: all-red → red+yellow → green → yellow →
all-red, alternating which direction gets to go. This implements exactly that, using
the same "state returns next state" pattern.

```python
from machine import Pin
from time import sleep

# Nord-Syd
ns_red, ns_yellow, ns_green = Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT)
# Øst-Vest
ev_red, ev_yellow, ev_green = Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)

def set_lights(ns, ev):
    ns_red.value(ns[0]); ns_yellow.value(ns[1]); ns_green.value(ns[2])
    ev_red.value(ev[0]); ev_yellow.value(ev[1]); ev_green.value(ev[2])

def all_red():
    set_lights((1,0,0), (1,0,0))
    sleep(1.0)
    return ns_ready

def ns_ready():        # NS: red+yellow (about to go)
    set_lights((1,1,0), (1,0,0))
    sleep(1.0)
    return ns_go

def ns_go():            # NS: green
    set_lights((0,0,1), (1,0,0))
    sleep(5.0)
    return ns_stop

def ns_stop():          # NS: yellow
    set_lights((0,1,0), (1,0,0))
    sleep(1.5)
    return all_red2

def all_red2():
    set_lights((1,0,0), (1,0,0))
    sleep(1.0)
    return ev_ready

def ev_ready():          # EV: red+yellow
    set_lights((1,0,0), (1,1,0))
    sleep(1.0)
    return ev_go

def ev_go():              # EV: green
    set_lights((1,0,0), (0,0,1))
    sleep(5.0)
    return ev_stop

def ev_stop():            # EV: yellow
    set_lights((1,0,0), (0,1,0))
    sleep(1.5)
    return all_red

state = all_red
while state:
    state = state()
```

---

## 3. Random state machine (matches your slide 5 diagram exactly)

State0/State1/State2 with `random() >= 0.5` transitions, plus a `Stop` state.
LEDs stand in for each state so it's visible on the board, not just printed.

```python
from machine import Pin
from random import random
from time import sleep

led0 = Pin(0, Pin.OUT)   # State0
led1 = Pin(1, Pin.OUT)   # State1
led2 = Pin(2, Pin.OUT)   # State2

def all_off():
    led0.off(); led1.off(); led2.off()

def state0():
    all_off(); led0.on()
    print("State0")
    sleep(1)
    return state1 if random() >= 0.5 else state2

def state1():
    all_off(); led1.on()
    print("State1")
    sleep(1)
    return state0 if random() >= 0.5 else state2

def state2():
    all_off(); led2.on()
    print("State2")
    sleep(1)
    if random() < 0.5:
        return None   # -> Stop
    return state0 if random() >= 0.5 else state0

state = state0
while state:
    state = state()

all_off()
print("Stop")
```

---

## 4. Elevator state machine — your 2 buttons as Up/Down

Matches the "Main / 2nd" elevator diagram: pressing the floor you're already on does
nothing (self-loop). Shows current floor on the 7-segment digit if you have the
segment pins — otherwise it just prints.

```python
from machine import Pin
from time import sleep

btn_up = Pin(6, Pin.IN, Pin.PULL_UP)     # confirmed button1
btn_down = Pin(7, Pin.IN, Pin.PULL_UP)   # ASSUMED button2

def wait_release(btn):
    while btn.value() == 0:
        sleep(0.05)

def main_floor():
    print("Floor: Main")
    while True:
        if btn_up.value() == 0:
            wait_release(btn_up)
            return second_floor
        sleep(0.05)

def second_floor():
    print("Floor: 2nd")
    while True:
        if btn_down.value() == 0:
            wait_release(btn_down)
            return main_floor
        sleep(0.05)

state = main_floor
while True:
    state = state()
```

---

## 5. "Livets gang" — Home / Work / Bed with a weekday restriction

Your slide 15 task adds a time restriction ("weekends") to the Home→Work→Bed cycle.
Since the Pico has no real calendar by default, this simulates days with a counter
(`day_count % 7`), matching the spirit of the exercise without needing RTC setup.

```python
from time import sleep

day_count = 0   # 0=Mon ... 5=Sat, 6=Sun

def is_weekend():
    return day_count % 7 >= 5

def home(x):
    global day_count
    if x == "wake":
        if is_weekend():
            print(f"Day {day_count}: Weekend - staying home")
            sleep(1)
            day_count += 1
            return home("wake")
        print(f"Day {day_count}: Take train to work")
        sleep(1)
        return work("arrived")
    if x == "tired":
        print(f"Day {day_count}: Going to bed")
        sleep(1)
        return bed("sleep")
    return None

def work(x):
    print(f"Day {day_count}: Working")
    sleep(1)
    print("Take train home")
    return home("tired")

def bed(x):
    global day_count
    if x == "sleep":
        print(f"Day {day_count}: Sleeping")
        sleep(1)
        day_count += 1
        print("Wake up")
        return home("wake")
    return None

state = home("wake")
count = 0
while state and count < 21:   # run 3 simulated weeks then stop
    state = state[0](state[1]) if isinstance(state, tuple) else state
    count += 1

print("Done with life!")
```

*Note:* this one is intentionally a bit different in structure from the slide's exact
pattern — your teacher's `Home(x)`/`Work(x)`/`Bed(x)` functions take a string and
return the next function call directly (not a `(func, arg)` tuple). If your exam wants
that exact calling convention, write it as:

```python
def home(x):
    ...
    return work("arrived")   # call the next function immediately, don't just return it

state = home("wake")
while state:
    state = state   # each function already calls the next one internally
```
which is simpler but loses the `while state: state=state()` outer loop — match
whichever convention your teacher used in the source `.py` file, if you have it.

---

## 6. PWM brightness control via buttons (the actual PWM.pptx slide 16 task)

"Brug knapperne til at skrue op og ned for LED'en" — one button raises brightness,
the other lowers it, clamped to 0–100%, no crashes at either extreme.

```python
from machine import Pin, PWM
from time import sleep

btn_up = Pin(6, Pin.IN, Pin.PULL_UP)     # confirmed
btn_down = Pin(7, Pin.IN, Pin.PULL_UP)   # ASSUMED

led_pwm = PWM(Pin(0))
led_pwm.freq(1000)   # fixed safe carrier frequency, see earlier freq-too-small note

brightness_pct = 0
STEP = 5

try:
    while True:
        if btn_up.value() == 0:
            brightness_pct = min(100, brightness_pct + STEP)
            sleep(0.15)   # debounce-ish
        elif btn_down.value() == 0:
            brightness_pct = max(0, brightness_pct - STEP)
            sleep(0.15)

        duty = int(brightness_pct / 100 * 65535)
        led_pwm.duty_u16(duty)
except KeyboardInterrupt:
    led_pwm.duty_u16(0)
    led_pwm.deinit()
```

---

## 7. Battery-voltage indicator (Spændingsdeler_Pico.xlsx)

Your spreadsheet defines thresholds: green=12V, yellow=8V, red=4V, red-blinking=2V,
read through a voltage divider into an ADC pin. Pico's ADC reads 0–3.3V as 0–65535,
so the divider must scale the real battery voltage down into that range — check your
divider's resistor values to get the correct scale factor (`SCALE` below is a
placeholder, replace with `R2 / (R1 + R2)` from your actual divider, and `VREF`/ADC
max with what your circuit produces).

```python
from machine import Pin, ADC
from time import sleep

adc = ADC(Pin(26))   # ASSUMED ADC pin — confirm yours
green = Pin(2, Pin.OUT)
yellow = Pin(1, Pin.OUT)
red = Pin(0, Pin.OUT)

SCALE = 12 / 3.3   # placeholder: real_voltage = adc_voltage * SCALE -- verify against your divider

def read_voltage():
    raw = adc.read_u16()
    adc_voltage = (raw / 65535) * 3.3
    return adc_voltage * SCALE

def all_off():
    green.off(); yellow.off(); red.off()

while True:
    v = read_voltage()
    all_off()
    if v >= 10:
        green.on()
    elif v >= 6:
        yellow.on()
    elif v >= 3:
        red.on()
    else:
        # red blinking = critical, below ~2V
        red.on()
        sleep(0.2)
        red.off()
        sleep(0.2)
        continue
    sleep(0.5)
```

---

## Patterns the exam seems to reward (from your two graded attempts + these slides)

- **Function-based state machines** (`state = state()`) are the taught structure for
  anything sequential (traffic lights, elevators, life-cycle sims) — prefer this over
  a flat `if/elif` chain inside one `while True`.
- **Buttons should always be read, never left declared-but-unused.**
- **PWM**: never call `.freq()` with `0` or anything below ~8 Hz on the RP2040; keep a
  fixed safe carrier frequency and do user-facing "blink speed" in software with
  `sleep()`, not via `.freq()`.
- **Always clamp/validate user or sensor input** (`min()`/`max()`, range checks) rather
  than trusting it'll be in bounds.
- **Clean shutdown**: `except KeyboardInterrupt`, set outputs to a safe state (off /
  duty 0), `deinit()` any PWM objects.
