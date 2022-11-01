# Boxcar with ADC

The ADS1256 is a 24-bit, 8-channel, 30 kSps ADC chip. The chip outputs are in SPI mode, so it cannot be directly read from USB interface. A seperate STM32 chip is used to convert the SPI data into buffer and send the data to computer via USB. The STM32 controller also handles trigger input, integration switch signal generation, etc.

The server can also be used with 12 bit built in ADC of STM32, which has over 3.6 MSps sampling rate.