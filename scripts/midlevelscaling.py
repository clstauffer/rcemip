""""
Catherine Stauffer -- EOAS Department, FSU

Function for calculating the scaling diagnostic for mid-level clouds as described by Cronin and Wing (2017)

Last updated -- 15 November 2021
"""
def calc_relh(qv, tair, phPa):
    """
    Calculate relative humidity
    INPUT
        qv: unsaturated environment vapor mixing ratio
        tair: temperature [K]
        phPa: pressure [hPa]
    OUTPUT
        relh: relative humidity [-]
    """

    esat = calc_esat(tair)
    qsat = 0.622*esat/(phPa-esat)
    relh = 0.001*qv/qsat

    return(relh)

def calc_esat(tair):
    """
    Calculates saturation vapor pressure
    INPUT
        tair: temperature [K]
    OUTPUT
        esat: saturation vapor pressure Pa
    """

    import numpy as np

    tmax_ice = 0
    tmin_ice = -20
    tair=tair-273.15

    esatw_coeffs = [6.11239921, 0.443987641, 0.142986287e-1, 0.264847430e-3,
                    0.302950461e-5, 0.206739458e-7, 0.640689451e-10,
                    -0.952447341e-13, -0.976195544e-15
                   ]

    esati_coeffs = [6.11147274, 0.503160820, 0.188439774e-1, 0.420895665e-3,
                    0.615021634e-5, 0.602588177e-7, 0.385852041e-9,
                    0.146898966e-11, 0.252751365e-14
                   ]

    esatw = np.zeros(np.shape(tair))
    esati = np.zeros(np.shape(tair))

    for index,coeffs in enumerate(zip(esatw_coeffs,esati_coeffs)):
        esatw = esatw + coeffs[0]*tair**(index)
        esati = esati + coeffs[1]*tair**(index)

    f_ew = (tair>tmax_ice) + (tair<=tmax_ice)*(tair>tmin_ice)*(tair-tmin_ice)/(tmax_ice-tmin_ice)
    f_ei = 1 - f_ew

    esat = f_ew * esatw + f_ei * esati
    esat = (esat*((tair+273.15)>185)) + ((0.00763685 + (tair*(0.000151069+(tair*7.48215e-07))))*((tair+273.15)<=185))
    return(esat)

def midlevelscaling(condstatsfile):
    """
    Calculates mid-level scaling of Cronin and Wing 2017 as used in Stauffer and Wing (2022)
    INPUT
        condstatsfile: conditional statistics file
    OUTPUT
        dsv: dataset of temporal-mean conditional statistics variables
             as well as derived-variables for the scaling and the scaling
    """

    from scipy import integrate
    import xarray as xr
    import numpy as np

    f = xr.open_dataset(condstatsfile)

    var      = ['TABS','CLD','COR','DSE','DSECDN','DSECLD','DSECOR',
                'DSEENV','ENV','MC','MCDNU','MCRUP','MCUP','MSE','QNENV',
                'QNSUP','QPENV','QPSUP','QTENV','QTSUP','RADQR','RHO',
                'SDN','SUP','TACOR','TASDN','TASUP','WCOR','WENV','WSDN',
                'WSUP']
    var_mean = ['tabs_mean','cld_mean','cor_mean','dse_mean','dsecdn_mean',
                'dsecld_mean','dsecor_mean','dseenv_mean','env_mean',
                'mc_mean','mdnu_mean','mcrup_mean','mcup_mean','mse_mean',
                'qnenv_mean','qnsup_mean','qpenv_mean','qpsup_mean',
                'qtenv_mean','qtsup_mean','radqr_mean','rho_mean','sdn_mean',
                'sup_mean','tacor_mean','tasdn_mean','tasup_mean','wcor_mean',
                'wenv_mean','wsdn_mean','wsup_mean']

    varmean = {}
    tabsmean = f.TABS.mean(axis=0)
    cold_trop = tabsmean.argmin().values+1
    varmean['trop']=cold_trop
    height = f.z
    pres = f.p
    varmean[var_mean[0]] = tabsmean

    for i in range(1,len(var_mean)):
        varmean[var_mean[i]] = f[var[i]].mean(axis=0)

    varmean['vc_mean'] = varmean['mc_mean'] * varmean['tabs_mean'] * 287 / (100 * pres) # cloud volume flux
    varmean['vcup_mean'] = varmean['mcup_mean'] * varmean['tabs_mean'] * 287 / (100 * pres) # updraft volume flux
    varmean['vcrup_mean'] = varmean['mcrup_mean'] * varmean['tabs_mean'] * 287 / (100 * pres) # updraft core volume flux
    varmean['vdnu_mean'] = varmean['mdnu_mean'] * varmean['tabs_mean'] * 287 / (100 * pres) # unsaturated downdraft volume flux
    varmean['supdn_mean'] = varmean['sup_mean'] + varmean['sdn_mean']
    varmean['wcld_mean'] = (varmean['wsup_mean'] * varmean['sup_mean'] + varmean['wsdn_mean'] * varmean['sdn_mean']) / varmean['supdn_mean']
    varmean['venv_mean'] = varmean['env_mean'] * varmean['wenv_mean'] # volume flux in unsaturated environment
    varmean['qvsup_mean'] = varmean['qtsup_mean'] - varmean['qnsup_mean'] # saturated updraft vapor mixing ratio
    varmean['qvenv_mean'] = varmean['qtenv_mean'] - varmean['qnenv_mean'] # unsaturated environment vapor mixing ratio
    varmean['deltas_mean'] = 1004 * (varmean['dsecld_mean'] - varmean['dseenv_mean']) * varmean['rho_mean'] # mean dry static energy excess per unit volume of cloudy air relative to environment
    varmean['dscor_mean'] = 1004 * (varmean['dsecor_mean'] - varmean['dsecdn_mean']) * varmean['rho_mean']

    varmean['rhenv_mean'] = calc_relh(varmean['qvenv_mean'], varmean['tabs_mean'], pres)

    Gamma_mean = (np.array(varmean['tabs_mean'][:-2]) - np.array(varmean['tabs_mean'][2:])) / (np.array(height[2:])-np.array(height[:-2]))
    varmean['Gamma_mean'] = np.concatenate([[1e5],Gamma_mean,[1e5]]) # centered-difference approx to lapse rate

    varmean['JT_mean'] = (varmean['radqr_mean'] * varmean['rho_mean'] * 1004) / (86400 * varmean['Gamma_mean'])
    Jp_int  = integrate.cumtrapz(varmean['radqr_mean'] * 1004 / 86400,-100 * pres / 9.81)
    varmean['Jp_int']  = np.concatenate([(min(Jp_int) - Jp_int),[0]])

    ijx = np.argwhere(np.array(varmean['Jp_int']) == max(np.array(varmean['Jp_int'])))[1][0]+1
    ijn = np.argwhere(np.array(varmean['wcld_mean']) > 0)[0][0]+1

    cld_scaling = np.empty(np.shape(varmean['cld_mean']), float)
    cld_scaling.fill(np.nan)

    A = -1 * varmean['Jp_int'][ijn:ijx]
    B = varmean['wcld_mean'][ijn:ijx]
    C = 2.5e6*100
    D = calc_esat(varmean['tabs_mean'][ijn:ijx])
    E = 1 - varmean['rhenv_mean'][ijn:ijx]
    F = 461*varmean['tabs_mean'][ijn:ijx]
    G = varmean['dscor_mean'][ijn:ijx]
    cld_scaling[ijn:ijx] = A/(B*((C*D*E/F)+G))

    varmean['cld_scaling'] = cld_scaling

    dsv = xr.Dataset(varmean)
    return(dsv)

def interpvertprofs(mls295,mls300,mls305,z295,z300,z305,t295,t300,t305):
    """
    Calculates the evenly-spaced vertical profiles used for interpolation
    INPUT
        mls295,mls300,mls305: mid-level scaling profiles to determine
                              mid-level range the metric will focus on
        z295,z300,z305: height profiles [m] to create an interpolation
                        profile from
        t295,t300,t305: temperature profiles [K] to create an interpolation
                        profile from
    OUTPUT
        zavg: interpolation height profile [m]
        tavg: interpolation temperature profile [K]
    """

    import numpy as np

    def split_list(a_list):
        """
        function to split array in two parts
        """
        half = len(a_list)//2
        return a_list[:half], a_list[half:]
    def findrange(ccc):
        """
        function to find the low-level and upper-level maxima
        and the mid-level minima
        """
        bbb,ttt = split_list(ccc)
        b = np.asarray(np.where(ccc==max(bbb)))[0][0]
        t = np.asarray(np.where(ccc==max(ttt)))[0][-1]
        m = np.asarray(np.where(ccc==min(ccc[b:t])))[0][0]
        return(b,m,t)


    __,imid295,itop295 = findrange(mls295)
    __,imid300,itop300 = findrange(mls300)
    __,imid305,itop305 = findrange(mls305)

    ### find the lowest mid-level index which is the lowest point in the atmosphere of the SSTs
    imid=max([imid295,imid300,imid305])
    ### find the highest high-level index which is the highest point in the atmosphere of the SSTs
    itop=min([itop295,itop300,itop305])
    ### average length of the array from imid-imax for the average vertical profiles
    lavg=int(round(np.average([len(mls295[imid:itop+1]),len(mls300[imid:itop+1]),len(mls305[imid:itop+1])])))

    ### average profiles for interpolation
    tmin=max([t295[itop295],t300[itop300],t305[itop305]])
    tmax=min([t295[imid295],t300[imid300],t305[imid305]])
    tavg = np.linspace(tmin,tmax,lavg) #goes top to bottom
    zmax=min([z295[itop295],z300[itop300],z305[itop305]])
    zmin=max([z295[imid295],z300[imid300],z305[imid305]])
    zavg=np.linspace(zmin,zmax,lavg) #goes top to bottom

    return(tavg,zavg)

def intavg(xx295,xx300,xx305,yy295,yy300,yy305,yyavg,vinv):
    """
    Function to interpolate profiles of 295, 300, and 305 to a common axis
    INPUT
        xx295,xx300,xx305: variable profiles to interpolate to a common
                           vertical profile, yyavg
        yy295,yy300,yy305: vertical profiles
        yyavg: vertical profile used for interpolation
               calculated in interpvertprofs
        vinv: boolean, True for temperature axis False for height axis
    OUTPUT
        xxint295,xxint300,xxint305: interpolated profiles
        xxintavg: average profile of the interpolated profiles
        xxintrng: profile of the range of the interpolated profiles
                  (max - min for each level)
        xxintdif: profile of the difference of the interpolated profiles
                  (305 - 295 for each level)
    """
    import numpy as np
    from scipy import interpolate

    def finterp(y_mean,x_full,y_full):
        """
        interpolates x values (x_full) with individual
        y values (y_full) to a common y value (y_mean)
        """
        tck = interpolate.splrep(y_full,x_full)
        x_mean = interpolate.splev(y_mean, tck)
        return(x_mean)

    # interpolates the x-axis and y-axis to the limited-range y-axis
    if vinv == True: # inverse the arrays, used for the temperature interpolation
        xxint295= finterp(yyavg,xx295[::-1],yy295[::-1])
        xxint300= finterp(yyavg,xx300[::-1],yy300[::-1])
        xxint305= finterp(yyavg,xx305[::-1],yy305[::-1])
    if vinv == False:
        xxint295= finterp(yyavg,xx295,yy295)
        xxint300= finterp(yyavg,xx300,yy300)
        xxint305= finterp(yyavg,xx305,yy305)

    # average profile across 295, 300, and 305
    xxintavg = np.average([xxint295,xxint300,xxint305],axis=0)

    # caluclates 305-295 as well as the range in the data
    xxintdif,xxintrng=[],[]
    for i in range(len(yyavg)):
        xxintrng.append(max([xxint295[i],xxint300[i],xxint305[i]])-min([xxint295[i],xxint300[i],xxint305[i]]))
        xxintdif.append(xxint305[i]-xxint295[i])

    return(xxint295,xxint300,xxint305,xxintavg,xxintrng,xxintdif)

def mlsmetric(var295,var300,var305,trop295,trop300,trop305,z295,z300,z305,zavg,t295,t300,t305,tavg):
    """
    Calculates the metrics for mid-level cloud fraction analysis used in Stauffer and Wing (2022)
    INPUT
        var295,var300,var305: variable profiles
        trop295,trop300,trop305: tropopause index, calculated in midlevelscaling
        z295,z300,z305,zavg: height profiles including interpolation profile
                             calculated in interpvertprofs
        t295,t300,t305,tavg: temperature profiles including interpolation profile
                             calculated in interpvertprofs
    OUTPUT
        mets: dictionary of average height, range height and temperature,
              and difference height and temperature profile metrics
    """
    import numpy as np

    # limit profiles to the troposphere
    lowesttrop = min([trop295,trop300,trop305])
    var295,var300,var305 = var295[:lowesttrop],var300[:lowesttrop],var305[:lowesttrop]
    z295,z300,z305 = z295[:lowesttrop],z300[:lowesttrop],z305[:lowesttrop]
    t295,t300,t305 = t295[:lowesttrop],t300[:lowesttrop],t305[:lowesttrop]

    # temperature axis interpolation
    __,__,__,vartavg,vartrng,vartdif = intavg(var295,var300,var305,t295,t300,t305,tavg,True)
    # height axis interpolation
    __,__,__,varzavg,varzrng,varzdif = intavg(var295,var300,var305,z295,z300,z305,zavg,False)

    # collapse profiles to one number (vertical average)
    varzavgm = np.average(varzavg)
    vartavgm = np.average(vartavg)
    vartrngm = np.average(vartrng)
    varzrngm = np.average(varzrng)
    vartdifm = np.average(vartdif)
    varzdifm = np.average(varzdif)

    mets={'Average Height Profile Metric':varzavgm,'Average Temperature Profile Metric':vartavgm,
          'Range Height Profile Metric':varzrngm,'Range Temperature Profile Metric':vartrngm,
          'Difference Height Profile Metric':varzdifm,'Difference Temperature Profile Metric':vartdifm
         }

    return(mets)

def ratio(t,a,b,e,f,g):
    """
    Saves the numerator and denominator separately for the mid-level 
        scaling diagnostic (Equation 5 in Cronin and Wing, 2017 and Stauffer and Wing, 2020)
    INPUT
        t: temperature [K]
        a: Jp_int (calculated in midlevelscaling)
        b: wcld
        e: rhenv
        f: temperature [K]
        g: dscor
    OUTPUT
        num: the numerator; troposphere integrated radiative-cooling
        dem: the denominator; flux of xyz
    """

    a = -1*a
    e = 1-e
    f = 461*f
    d = calc_esat(t)
    c = 2.5e6*100

    num = a
    dem = (b*((c*d*e/f)+g))
    return(num,dem)
