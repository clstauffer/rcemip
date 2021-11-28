""""
Catherine Stauffer -- EOAS Department, FSU

Function for calculating cloud fraction definitions as described by Stauffer and Wing (2022)

Last updated -- 15 November 2021
"""
def calc_qsatw(tair, phPa):
    """
    Calculates saturation vapor pressure over water
    INPUT
        tair: temperature [K]
        phPa: pressure [Pa]
    OUTPUT
        qstaw: saturation mixing ratio over water
    """

    import numpy as np

    tmax_ice = 0
    tmin_ice = -20
    tair = tair-273.15 # convert temperature from K to C

    esatw_coeffs = [6.11239921, 0.443987641, 0.142986287e-1, 0.264847430e-3,
                    0.302950461e-5, 0.206739458e-7, 0.640689451e-10,
                    -0.952447341e-13, -0.976195544e-15
                   ]
    esatw = np.zeros(np.shape(tair))

    for index,coeffs in enumerate(esatw_coeffs):
        esatw = esatw + coeffs*tair**(index)

    f_ew = (tair>tmax_ice) + (tair<=tmax_ice)*(tair>tmin_ice)*(tair-tmin_ice)/(tmax_ice-tmin_ice)
    esat = f_ew * esatw
    esat = (esat*((tair+273.15)>185)) + ((0.00763685 + (tair*(0.000151069+(tair*7.48215e-07))))*((tair+273.15)<=185))
    qsatw = 0.622*esat/(phPa-esat)

    return(qsatw)

def cloudfraction(cw,ci,ta,pa):
    """
    Calculates cloud fraction definitions cfv1 and cfv2 used in <paper>
    INPUT
        cw: cloud water condensate [g/g]
        ci: cloud ice condensate [g/g]
        ta: temperature [K]
        pa: pressure [Pa]
    OUTPUT
        cfv1: cloud fraction using a threshold value of
              cloud condensate of 10−5 gg−1 or 1% of the saturation
              mixing ratio over water, whichever is smaller
        cfv2: cloud fraction using a threshold value of
              cloud condensate of 10−5 gg−1
    """

    import numpy as np

    tw = np.add(cw,ci)
    qsatw = calc_qsatw(ta,pa)
    cfv1   = (tw > np.minimum((0.01*qsatw),(1e-5))).astype(int)
    cfv2   = (tw > (1e-5)).astype(int)

    return(cfv1,cfv2)
