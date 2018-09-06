import sys
import Adafruit_DHT


# Parametros de letura, tipo de sensor y pin
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    sys.exit(1)

# Intenta leer temperatura.  
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

#Si no obtiene lectura del sensor, termina el programa
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
