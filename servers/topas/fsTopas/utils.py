def wavenumber_to_nanometer(wn:float) -> float:
    """wavenumber (cm-1) is just the inverse of wavelength in cm"""
    return 1/(wn*100) * (10**9)


def nanometer_to_wavenumber(nm:float) -> float:
    return 0.01/(nm/(10**9))

