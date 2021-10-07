def ps_to_mm(ps:float) -> float:
    """v = 1.0003 in air, so
    speed of light = 299,702,547 meters per second in air.
    For a retroreflector delay line setup, the light travels
    forth and back so the optical path difference is twice
    the distance traveled by mirror, thus the division by 2
    """
    return ps*0.299702547*0.5


def mm_to_ps(mm:float) -> float:
    """the above function reversed"""
    return 2*mm/0.299702547


def wavenumber_to_nanometer(wn:float) -> float:
    """wavenumber (cm-1) is just the inverse of wavelength in cm"""
    return 1/(wn*100) * (10**9)


def nanometer_to_wavenumber(nm:float) -> float:
    return 0.01/(nm/(10**9))

