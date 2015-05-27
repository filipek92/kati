# Pinout of the header at RPi 2

### I2C
| Pin number | Function | IN/OUT |
|:---:|:---:|:---:|
| 3 | SDA | IN/OUT |
| 5 | SCL | OUT |

### Serial port
| Pin number | Function | IN/OUT |
|:---:|:---:|:---:|
| 8 | TXD | OUT |
| 10 | RXD | IN |

### Card readers
| Indoor reader | Outdoor reader | Function | IN/OUT |
|:---:|:---:|:---:|:---:|
| 18 | 32 | Beeper (yellow) | OUT |
| 19 | 33 | Hold (blue) | OUT |
| 21 | 35 | Data 0 (green) | IN |
| 22 | 36 | Data 1 (white) | IN |
| 23 | 37 | Green LED (orange) | OUT |
| 24 | 38 | Red LED (brown) | OUT |
| 26 | 40 | Tamper (violet) | IN |

### Lock
| Pin number | Function | IN/OUT |
|:---:|:---:|:---:|
| 11 | HIGH: locked, LOW: open | OUT |

### Tamper
| Pin number | Function | IN/OUT |
|:---:|:---:|:---:|
| 15 | HIGH: tampered, LOW: OK | IN |
