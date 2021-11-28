""""
Catherine Stauffer -- EOAS Department, FSU

Function for calculating conditional statistics as used in Stauffer and Wing (2022)

Last updated -- 15 November 2021
"""
def domainavg(var):
    import numpy as np
    return(np.nanmean(var,axis=(1,2)))

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

def calcstat(cw,ci,pw,pi,ta,pa,wa,qv,radqr,z,time,cldver='cfv2'):

    """
    Calculates cells that have a cloud, core, saturated, unsaturated
    INPUT
        Note: all but time and cldver are 3D arrays of (z,y,x)
        cw: cloud liquid water [g/g]
        ci: cloud ice [g/g]
        pw: precipitating liquid water [g/g]
        pi: precipitating ice [g/g]
        ta: temperature [K]
        pa: pressure [Pa]
        wa: vertical wind component [m/s]
        qv: water vapor specific humidity [g/g]
        radqr: radiative heating rate [K/s]
        z: height [m]
        time: time [hr]
        cldver: cloud fraction definition to use as defined in
                Stauffer and Wing, default is cfv2
    OUTPUT
        cstats: xarray dataset of conditional statistics, units
                and description are commented next to the variables
                starting at line 199
    """

    import xarray as xr
    import numpy as np


    tw = np.add(cw,ci)
    del cw,ci

    tp = np.add(pw,pi)
    del pw,pi

    qsatw = calc_qsatw(ta,pa)
    rho = pa/(287*ta)

    wi = np.concatenate((np.zeros((1,np.shape(wa)[1],np.shape(wa)[2])),wa),axis=0)
    w  = np.add(wi[:-1,:,:],wi[1:,:,:])
    del wi

    tmps = ta*((1000/pa)**0.2854)
    tvirt = tmps*(1+0.61*qv-(tw)-(tp))
    del tmps

    tvz = np.mean(tvirt,axis=(1,2))
    tva = np.repeat(tvz,(np.shape(tvirt)[1]*np.shape(tvirt)[2])).reshape(np.shape(tvirt))
    del tvz

    gamaz = 9.81*z/1004
    lvcp  = 2.501e6/1004
    dse = ta+gamaz
    mse = dse+(lvcp*qv)

    qt = qv+tw

    if cldver == 'cfv1':
        cldy = np.minimum((0.01*qsatw),(1e-5))
    if cldver == 'cfv2':
        cldy = (1e-5)

    cld   = (tw > cldy).astype(int)                # cloud fraction
    cor   = ((tvirt > tva) & (w > 2)).astype(int)  # core fraction
    cordn = ((tvirt < tva) & (w < -2)).astype(int) # downdraft core fraction
    satup = ((tw > cldy) & (w >= 0)).astype(int)   # saturated updraft fraction
    satdn = ((tw > cldy) & (w < 0)).astype(int)    # saturated downdraft fraction
    env   = ((tw <= cldy)).astype(int)             # cloud-free environment fraction

    hydro = ((tw > cldy) | (tp > 1e-4)).astype(int)                        # hydrometer fraction
    mcup  = (((tw > cldy) & (0.5*w>0)).astype(int))*(rho*0.5*w)            # updraft cloud mass flux
    mcdns = (((tw > cldy) & (0.5*w<=0)).astype(int))*(rho*0.5*w)           # downdraft saturated cloud mass flux
    mcdnu = (((tw <= cldy) & (tp > 1e-4) & (w<0)).astype(int))*(rho*0.5*w) # downdraft unsaturated cloud mass flux
    mc    = mcup+mcdns+mcdnu                                               # cloud mass flux
    mcrup = ((tvirt > tva) & (w > 2)).astype(int)*(rho*0.5*w)              # updraft core mass flux

    dsecdn = ((tvirt < tva) & (w < -2)).astype(int)*dse
    dsecld = (tw > cldy).astype(int)*dse
    dsecor = ((tvirt > tva) & (w > 2)).astype(int)*dse
    dseenv = ((tw <= cldy)).astype(int)*dse

    dsecdn[dsecdn==0] = np.nan
    dsecld[dsecld==0] = np.nan
    dsecor[dsecor==0] = np.nan
    dseenv[dseenv==0] = np.nan

    tacor = ((tvirt > tva) & (w > 2)).astype(int)*ta
    tasdn = ((tw > cldy) & (w < 0)).astype(int)*ta
    tasup = ((tw > cldy) & (w >= 0)).astype(int)*ta

    tacor[tacor==0] = np.nan
    tasup[tasup==0] = np.nan
    tasdn[tasdn==0] = np.nan

    wcor = ((tvirt > tva) & (w > 2)).astype(int)*wa
    wenv = ((tw <= cldy)).astype(int)*wa
    wsdn = ((tw > cldy) & (w < 0)).astype(int)*wa
    wsup = ((tw > cldy) & (w >= 0)).astype(int)*wa

    wcor[wcor==0] = np.nan
    wsdn[wsdn==0] = np.nan
    wsup[wsup==0] = np.nan
    wenv[wenv==0] = np.nan

    qnsup = (((tw > cldy) & (w >= 0)).astype(int)*tw)*1000
    qnenv = (((tw <= cldy)).astype(int)*tw)*1000
    qpsup = (((tw > cldy) & (w >= 0)).astype(int)*tp)*1000
    qpenv = (((tw <= cldy)).astype(int)*tp)*1000
    qtsup = (((tw > cldy) & (w >= 0)).astype(int)*qt)*1000
    qtenv = (((tw <= cldy)).astype(int)*qt)*1000

    qnsup[qnsup==0] = np.nan
    qpsup[qpsup==0] = np.nan
    qtsup[qtsup==0] = np.nan

    # domain averages
    cld   = (domainavg(cld)).reshape((len(time),len(z)))   # cloud fraction
    cor   = (domainavg(cor)).reshape((len(time),len(z)))   # core fraction
    cordn = (domainavg(cordn)).reshape((len(time),len(z))) # downdraft core fraction
    satup = (domainavg(satup)).reshape((len(time),len(z))) # saturated updraft fraction
    satdn = (domainavg(satdn)).reshape((len(time),len(z))) # saturated downdraft fraction
    env   = (domainavg(env)).reshape((len(time),len(z)))   # cloud-free environment fraction

    hydro = (domainavg(hydro)).reshape((len(time),len(z))) # hydrometer fraction
    mcup  = (domainavg(mcup)).reshape((len(time),len(z)))  # updraft cloud mass flux
    mcdns = (domainavg(mcdns)).reshape((len(time),len(z))) # downdraft saturated cloud mass flux
    mcdnu = (domainavg(mcdnu)).reshape((len(time),len(z))) # downdraft unsaturated cloud mass flux
    mc    = (domainavg(mc)).reshape((len(time),len(z)))    # cloud mass flux
    mcrup = (domainavg(mcrup)).reshape((len(time),len(z))) # updraft core mass flux

    rho   = (domainavg(rho)).reshape((len(time),len(z)))
    tabs  = (domainavg(ta)).reshape((len(time),len(z)))
    pa    = (domainavg(pa)/100).reshape((len(time),len(z)))
    radqr = (domainavg(radqr)*86400).reshape((len(time),len(z)))
    dse   = (domainavg(dse)).reshape((len(time),len(z)))
    mse   = (domainavg(mse)).reshape((len(time),len(z)))

    dsecdn = (domainavg(dsecdn)).reshape((len(time),len(z)))
    dsecld = (domainavg(dsecld)).reshape((len(time),len(z)))
    dsecor = (domainavg(dsecor)).reshape((len(time),len(z)))
    dseenv = (domainavg(dseenv)).reshape((len(time),len(z)))

    qnsup = (domainavg(qnsup)*1000).reshape((len(time),len(z)))
    qnenv = (domainavg(qnenv)*1000).reshape((len(time),len(z)))
    qpsup = (domainavg(qpsup)*1000).reshape((len(time),len(z)))
    qpenv = (domainavg(qpenv)*1000).reshape((len(time),len(z)))
    qtsup = (domainavg(qtsup)*1000).reshape((len(time),len(z)))
    qtenv = (domainavg(qtenv)*1000).reshape((len(time),len(z)))

    tacor = (domainavg(tacor)).reshape((len(time),len(z)))
    tasdn = (domainavg(tasdn)).reshape((len(time),len(z)))
    tasup = (domainavg(tasup)).reshape((len(time),len(z)))

    wcor  = (domainavg(wcor)).reshape((len(time),len(z)))
    wenv  = (domainavg(wenv)).reshape((len(time),len(z)))
    wsdn  = (domainavg(wsdn)).reshape((len(time),len(z)))
    wsup  = (domainavg(wsup)).reshape((len(time),len(z)))

    za  = (domainavg(z)).reshape((len(time),len(z)))
    zmean = np.mean(za,axis=0)
    pmean = np.mean(pa,axis=0)

    cstats = {
              'CLD':(('t','z'),cld),       # cloud fraction [-]
              'COR':(('t','z'),cor),       # core fraction [-]
              'CDN':(('t','z'),cordn),     # downdraft core fraction [-]
              'SUP':(('t','z'),satup),     # saturated updrafts fraction [-]
              'SDN':(('t','z'),satdn),     # saturated downdrafts fraction [-]
              'ENV':(('t','z'),env),       # unsaturated environment fraction [-]
              'HYDRO':(('t','z'),hydro),   # total fraction of hydrometeors [-]
              'MCUP':(('t','z'),mcup),     # updraft cloud mass flux [kg/m2/s]
              'MCDNS':(('t','z'),mcdns),   # downdraft saturated cloud mass flux [kg/m2/s]
              'MCDNU':(('t','z'),mcdnu),   # downdraft unsaturated mass flux [kg/m2/s]
              'MC':(('t','z'),mc),         # cloud mass flux [kg/m2/s]
              'MCRUP':(('t','z'),mcrup),   # updraft core mass flux [kg/m2/s]
              'RHO':(('t','z'),rho),       # air density [kg/m3]
              'TABS':(('t','z'),tabs),     # absolute temperature [K]
              'RADQR':(('t','z'),radqr),   # radiative heating rate [K/day]
              'DSE':(('t','z'),dse),       # dry static energy [K]
              'MSE':(('t','z'),mse),       # moist static energy [K]
              'DSECDN':(('t','z'),dsecdn), # mean dry static energy in downdraft core [K]
              'DSECLD':(('t','z'),dsecld), # mean dry static energy in cloud [K]
              'DSECOR':(('t','z'),dsecor), # mean dry static energy in core [K]
              'DSEENV':(('t','z'),dseenv), # mean dry static energy in unsaturated environment [K]
              'QNSUP':(('t','z'),qnsup),   # mean QN in saturated updrafts [g/kg]
              'QNENV':(('t','z'),qnenv),   # mean QN in unsaturated environment [g/kg]
              'QPSUP':(('t','z'),qpsup),   # mean QP in saturated updrafts [g/kg]
              'QPENV':(('t','z'),qpenv),   # mean QP in unsaturated environment [g/kg]
              'QTSUP':(('t','z'),qtsup),   # mean QT in saturated updrafts [g/kg]
              'QTENV':(('t','z'),qtenv),   # mean QT in unsaturated environment [g/kg]
              'TACOR':(('t','z'),tacor),   # mean TABS in core [K]
              'TASDN':(('t','z'),tasdn),   # mean TABS in saturated downdrafts [K]
              'TASUP':(('t','z'),tasup),   # mean TABS in saturated updrafts [K]
              'WCOR':(('t','z'),wcor),     # mean W in core [m/s]
              'WENV':(('t','z'),wenv),     # mean W in unsaturated environment [m/s]
              'WSDN':(('t','z'),wsdn),     # mean W in saturated downdrafts [m/s]
              'WSUP':(('t','z'),wsup),     # mean W in saturated updrafts [m/s]
              'p':(('z'),pmean)            # pressure [hPa]
             }
    coords = {
              't':time, # time [hr]
              'z':zmean # height [m]
             }

    cstats = xr.Dataset(cstats,coords)

    return(cstats)
