# Bladestorm

Bladestorm is an automation framework for PCTF/iCTF. In the "modules" directory, there is a sample module named "simplecalc.py". During the game, simply develop new modules according to the format of simplycalc.py, and you are ready to go.

## Installation

Install `swpag_client`:

```shell
$ sudo pip3 install swpag_client
```

Clone this repo:

```shell
$ git clone https://github.com/ret2basic/Bladestorm.git
```

## Usage

To run an module:

```shell
$ ./bladestorm.py <module_name> <args>
```

For example, to attack the "simplecalc" service (no arguments needed):

```shell
$ ./bladestorm.py simplecalc.py
```

To run Code Analyzer (uses directory as argument):

```shell
$ ./bladestorm.py code_analyzer <directory>
```

## Why This Name?

Here is the description of Bladestorm in WoW:

```plaintext
Become an unstoppable storm of destructive force, striking up to 8 nearby targets for [5 * ((50% of Attack power)% + (50% of Attack power)%)] Physical damage over 4 sec.

You are immune to movement impairing and loss of control effects, but can use defensive abilities and avoid attacks.
```

This is a perfect analogy for an attack/defense automation system.
