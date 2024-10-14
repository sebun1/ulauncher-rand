# Rand

An extension for ULauncher to generate random values.

## Installation

```
https://github.com/sebun1/ulauncher-rand
```

Install via the above URL in ULauncher preferences.

## Features

Commands:

- `n`/`num`: Generates a random number between 0 and n.
    - e.g. `rand n 0 100` or `rand num 0 100` for a number between 0 and 100.
- `i`/`int`: Generates a random integer between n and m.
    - e.g. `rand i 0 100` or `rand int 0 100` for an integer between 0 and 100.
- `c`/`coin`: Flips a coin.
    - e.g. `rand c` or `rand coin` to flip a coin.
- `d`/`dice`: Rolls a dice.
    - e.g. `rand d` or `rand dice` to roll a 6-sided die.
- `b`/`byte`: Generates random bytes in hex (default) or base64 (default 32 bytes).
    - e.g. `rand b 16 1` or `rand b 16 true` for 16 bytes in base64.

## Behaviors

- If provided arguments for a command are invalid, the default is used instead.
- Byte generation uses `os.urandom` while everything else uses `random`.
