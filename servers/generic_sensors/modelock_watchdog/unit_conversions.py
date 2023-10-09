from math import exp

def rh_to_ah(temperature_K, relative_humidity, air_density_SI=1.292, air_pressure_SI=101000):
    es = 611.2*exp(17.67*(temperature_K-273.15)/(temperature_K-29.65))
    rvs = 0.622*es/(air_pressure_SI - es)
    rv = relative_humidity/100. * rvs
    qv = rv/(1 + rv)
    absolute_humidity = qv*air_density_SI
    return absolute_humidity

