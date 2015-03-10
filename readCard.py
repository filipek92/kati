import RPi.GPIO as GPIO
import time

#CONSTANTS
numOfBits = 56

#PINOUTS
pins = {}
pins['data1'] = 24
pins['data0'] = 26

#CARDS
Buben029HEX = '6DAEA5FC'
Buben2011021HEX = '3DFBF628'
CVUT_PavelTHEX = '04345752DA2580'
comparisionCardHEX =Buben2011021HEX


def readDataHandler(pin):
  global bin
  global counter
  global lastReceivedTime

  if pin == pins['data0']:
    bin += '0'
  if pin == pins['data1']:
    bin += '1'

  counter += 1
  lastReceivedTime = time.time()
  if counter >= numOfBits:
    endOfTransfer(False)


def endOfTransfer(timeout):
  global bin
  global counter
  if timeout:
    print('Aborted')
  else:
    hexa = '%0*X' % ((len(bin) + 3) // 4, int(bin, 2))
    #DETERMINE CARD FORMAT
    if (hexa[10:14] == '0000'):
      CRC = '%0*X' % (2, int(hexa[0:2], 16) ^ int(hexa[2:4], 16) ^ int(hexa[4:6], 16) ^ int(hexa[6:8], 16))
      if hexa[8:10] == CRC:
        hexa = hexa[0:8]
    print(hexa)
  bin = ''
  counter = 0


#SET GPIOs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins['data1'], GPIO.IN)
GPIO.setup(pins['data0'], GPIO.IN)

#ADD HANDLERS TO INPUT PINS
GPIO.add_event_detect(pins['data1'], GPIO.FALLING, callback=readDataHandler)
GPIO.add_event_detect(pins['data0'], GPIO.FALLING, callback=readDataHandler)

counter = 0
bin = ''
lastReceivedTime = time.time()


try:
  while True:
    if (counter in range(1, numOfBits - 1)) and (time.time() - lastReceivedTime > 0.1):
      endOfTransfer(True)
    time.sleep(0.1)

except KeyboardInterrupt:
  GPIO.cleanup()
