""""
Catherine Stauffer -- EOAS Department, FSU

Function for calculating radiatively-driven divergence as described by Bony et al. (2016)

Last updated -- 15 November 2021
"""
def stability(pa,ta,theta):
    """
    Calculates static stability
    INPUT
        pa: pressure [Pa]
        ta: temperature [K]
        theta: potential temperature [K]
    OUTPUT
        S: static stability [K/Pa]
    """
    import numpy as np
    S = (ta/theta)*(np.gradient(theta)/(np.gradient(pa)))
    return(S)

def radiative_cooling(lwcs,swcs):
    """
    Calculates clear sky radiative cooling
    INPUT
        lwcs: clear-sky longwave radiative heating rate [K/s]
        swcs: clear-sky shortwave radiative heating rate [K/s]
    OUTPUT
        Qr: clear-sky radiative cooling rate [K/s]
    """
    Qr = (lwcs+swcs)
    return(Qr)

def radiative_subsidence(Qr,S):
    """
    Calculates radiative-subsidence velocity
    INPUT
        Qr: clear-sky radiative cooling rate [K/s]
        S: static stability [K/Pa]
    OUTPUT
        Or: radiative subsidence [Pa/s]
    """
    Or = Qr/S
    return(Or)

def radiative_divergence(Or,pa):
    """
    Calculates radiative-driven divergence
    INPUT
        Or: radiative subsidence [Pa/s]
        Pa: pressure [Pa]
    OUTPUT
        D: radiatively-driven divergence [1/s]
    """
    import numpy as np
    D = np.gradient(Or)/(np.gradient(pa))
    return(D)
