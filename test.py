from sense_emu import SenseHat
sense = SenseHat()

print(sense.temp)
print(sense.humidity)
print(sense.get_pressure())