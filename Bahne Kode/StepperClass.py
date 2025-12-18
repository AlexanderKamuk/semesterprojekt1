from machine import Pin, PWM
import time
import math


def _clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def _ease_cos(t):
    """Cosine ease-in-out (0..1 -> 0..1)."""
    return 0.5 - 0.5 * math.cos(math.pi * _clamp(t, 0.0, 1.0))


class StepperMotor:
    """Basic PWM stepper driver.

    - 4 pins: one motor
    - 8 pins: two motors (outer + inner wheel)

    Curve mode (8 pins + curve=True): inner wheel steps slower.
      - first 4 pins = outer/faster wheel
      - last 4 pins  = inner/slower wheel
    """

    def __init__(
        self,
        pins,
        step_mode="HALF",
        pwm_pct=30,
        frequency=20_000,
        micro_steps=4,
        curve=False,
        curve_intensity=1.0,
    ):
        self.pins = [PWM(Pin(p)) for p in pins]
        for pwm in self.pins:
            pwm.freq(int(frequency))

        self.pwm_max = 65535
        self.pwm_val = int(self.pwm_max * (float(pwm_pct) / 100.0))

        self.step_mode = str(step_mode).upper()
        self.micro_steps = max(1, int(micro_steps))

        self.curve = bool(curve)
        self.curve_intensity = _clamp(float(curve_intensity), 0.0, 1.0)

        self._step_index = 0
        self.step_counter = 0

        n = len(self.pins)
        if n not in (4, 8):
            raise ValueError("pins must be 4 (single motor) or 8 (two motors)")

        base4 = self._build_base_4pin_sequence()

        if n == 4:
            self.step_sequence = base4
        else:
            self.step_sequence = self._build_8pin_sequence_from_base(base4)

        self.stop_sequence = [0] * n
        self.stop()

    # sequences

    def _build_base_4pin_sequence(self):
        if self.step_mode == "FULL":
            return [
                [self.pwm_val, self.pwm_val, 0, 0],
                [0, self.pwm_val, self.pwm_val, 0],
                [0, 0, self.pwm_val, self.pwm_val],
                [self.pwm_val, 0, 0, self.pwm_val],
            ]

        if self.step_mode == "HALF":
            return [
                [self.pwm_val, 0, 0, 0],
                [self.pwm_val, self.pwm_val, 0, 0],
                [0, self.pwm_val, 0, 0],
                [0, self.pwm_val, self.pwm_val, 0],
                [0, 0, self.pwm_val, 0],
                [0, 0, self.pwm_val, self.pwm_val],
                [0, 0, 0, self.pwm_val],
                [self.pwm_val, 0, 0, self.pwm_val],
            ]

        if self.step_mode == "MICRO":
            # Simple linear microstepping (robust)
            ms = self.micro_steps
            step = max(1, self.pwm_val // ms)
            seq = []

            for i in range(ms):
                a = self.pwm_val - i * step
                b = i * step
                seq.append([a, b, 0, 0])
            for i in range(ms):
                b = self.pwm_val - i * step
                c = i * step
                seq.append([0, b, c, 0])
            for i in range(ms):
                c = self.pwm_val - i * step
                d = i * step
                seq.append([0, 0, c, d])
            for i in range(ms):
                d = self.pwm_val - i * step
                a = i * step
                seq.append([a, 0, 0, d])

            return seq

        raise ValueError("Invalid step_mode. Use 'FULL', 'HALF', or 'MICRO'.")

    def _build_8pin_sequence_from_base(self, base4):
        # Straight: both motors identical
        if (not self.curve) or (self.curve_intensity <= 0.01):
            return [s + s for s in base4]

        # Curve: inner wheel slower (outer:inner ratio)
        # intensity 1.0 => ratio 4 (strong curve)
        ratio = 1 + int(round(4.0 * self.curve_intensity))  # 1..4
        L = len(base4)
        seq = []
        for i in range(L * ratio):
            outer = base4[i % L]
            inner = base4[(i // ratio) % L]
            seq.append(outer + inner)
        return seq

    # low-level IO

    def set_step(self, values):
        for pwm, val in zip(self.pins, values):
            pwm.duty_u16(int(val))

    def stop(self):
        self.set_step(self.stop_sequence)

    # motion

    def _direction_to_step(self, direction):
        # Keep your original forward/backward wiring flip
        if direction == "forward":
            return -1
        if direction == "backward":
            return 1
        raise ValueError("direction must be 'forward' or 'backward'")

    def _step_once(self, direction_step, delay_us):
        n = len(self.step_sequence)
        self._step_index %= n
        self.set_step(self.step_sequence[self._step_index])
        time.sleep_us(int(delay_us))
        self._step_index = (self._step_index + direction_step) % n
        self.step_counter += direction_step

    def move_stepper(self, steps, direction, delay_us=900):
        direction_step = self._direction_to_step(direction)
        steps = abs(int(steps))
        for _ in range(steps):
            self._step_once(direction_step, delay_us)
        self.stop()

    def move_stepper_with_ramp(
        self,
        steps,
        direction,
        initial_delay_us=900,
        final_delay_us=450,
        ramp_steps=30,
    ):
        """Smooth ramp: ease-in -> steady -> ease-out."""
        direction_step = self._direction_to_step(direction)
        steps = abs(int(steps))
        if steps <= 0:
            return

        initial_delay_us = int(initial_delay_us)
        final_delay_us = int(final_delay_us)
        if final_delay_us < 120:
            final_delay_us = 120

        ramp_steps = int(ramp_steps)
        if ramp_steps < 1:
            ramp_steps = 1

        # Reach speed quicker, and keep ramp sane on short moves
        ramp_steps = min(ramp_steps, max(1, steps // 3))

        # Ramp up (decrease delay smoothly)
        for i in range(ramp_steps):
            t = (i + 1) / ramp_steps
            e = _ease_cos(t)
            delay = initial_delay_us + int((final_delay_us - initial_delay_us) * e)
            self._step_once(direction_step, delay)

        # Steady
        steady = steps - 2 * ramp_steps
        for _ in range(max(0, steady)):
            self._step_once(direction_step, final_delay_us)

        # Ramp down (increase delay smoothly)
        for i in range(ramp_steps):
            t = (i + 1) / ramp_steps
            e = _ease_cos(t)
            delay = final_delay_us + int((initial_delay_us - final_delay_us) * e)
            self._step_once(direction_step, delay)

        self.stop()
