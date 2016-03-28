# Pinout of the header at RPi 2

### I2C
| Pin/GPIO number | Function | IN/OUT |
|:---:|:---:|:---:|
| 3/2 | SDA | IN/OUT |
| 5/3 | SCL | OUT |

### Serial port
| Pin/GPIO number | Function | IN/OUT |
|:---:|:---:|:---:|
| 8/14 | TXD | OUT |
| 10/15 | RXD | IN |

### Card readers
| Indoor reader | Outdoor reader | Function | IN/OUT |
|:---:|:---:|:---:|:---:|
| 18/24 | 32/12 | Beeper (yellow) | OUT |
| 19/10 | 33/13 | Hold (blue) | OUT |
| 21/9 | 35/19 | Data 0 (green) | IN |
| 22/25 | 36/16 | Data 1 (white) | IN |
| 23/11 | 37/26 | Green LED (orange) | OUT |
| 24/8 | 38/20 | Red LED (brown) | OUT |
| 26/7 | 40/21 | Tamper (violet) | IN |

### Lock
| Pin/GPIO number | Function | IN/OUT |
|:---:|:---:|:---:|
| 11/17 | HIGH: locked, LOW: open | OUT |

### Tamper
| Pin/GPIO number | Function | IN/OUT |
|:---:|:---:|:---:|
| 15/22 | HIGH: tampered, LOW: OK | IN |
