# UPDATED 20210401 ************************************************************
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# FUNCTIONS TO PROCESS DATA ------------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def process_2D(model, domain, temperature, variable, mfiles, mtype, pmap=True):
    """
        Processes 2D data for all but LES/VER models

        Args:
            model: string, which model is being processed
                must be format in the directory system
            domain: string, which domain is being processed
            temperature: string, which SST is being processed
            variable: string, which variable is being processed
            mfiles: boolean, False for all variables and times are in one file
            mtype: string, denotes global or cartesian plane
            pmap: (optional, True) boolean,

        Returns:
            v: 3D array [time,x,y], the variable processed
            x: 1D array [x], zonal data (meters or degrees)
            y: 1D array [x], meridional data (meters or degrees)
            t: 1D array [t], time data (days)
    """

    # AXIS VARIABLE NAME
    if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'ICON_GCM':
        x = 'lat'
        y = 'lon'
    elif model == 'UCLA-CRM':
        x = 'xt'
        y = 'yt'
    elif mtype == 'GCM' or model == 'WRF-CRM':
        if model[0:7] == 'WRF_GCM':
            x = 'x'
            y = 'y'
        elif model == 'UKMO-GA7.1':
            x = 'longitude'
            y = 'latitude'
        else:
            x = 'lon'
            y = 'lat'
    elif model == 'WRF_COL_CRM':
        x = 'west_east'
        y = 'south_north'
    elif model == 'FV3':
        x = 'grid_xt'
        y = 'grid_yt'
    elif model[:5] == 'DALES':
        x = 'xm'
        y = 'ym'
    else:
        x = 'x'
        y = 'y'

    # MODEL PATH
    rcemip = '/huracan/tank2/columbia/RCEMIP/'
    if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'ICON_GCM':
        mpath  = rcemip+model+'/'+'RCE_'+domain+'_'+temperature+'/2D/'
    elif model[0:7] == 'WRF_GCM':
        mpath  = rcemip+'WRF_GCM/'+model[8:12]+'/RCE_'+domain+temperature+'/2D/'
    else:
        mpath  = rcemip+model+'/'+'RCE_'+domain+temperature+'/2D/'

    # FILE PATH
    if mfiles == True:
        if model == 'SAM6.11.2':
            f = rcemip+model+'/RCEMIP_upload/RCE_'+domain+temperature+'/2D/SAM_CRM_RCE_'+domain+temperature+'_2D_'+variable+'.nc'
        elif model == 'SAM_GCRM':
            f = mpath+model+'_RCE_'+domain+temperature+'_2D_'+pmap+'.nc'
        else:
            f = mpath+model+'_RCE_'+domain+temperature+'_2D_'+variable+'.nc'
    if mfiles == False:
        if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'ICON_GCM':
            if variable == 'sprw' and model != 'ICON_GCM':
                if model == 'ICON_LEM_CRM':
                    f = mpath+model+'-RCE_'+domain+'_'+temperature+'-2D_sprw_last25d.nc'
                if model == 'ICON_NWP_CRM':
                    f = mpath+model+'-RCE_'+domain+'_'+temperature+'-2D_sprw.nc'
            else:
                f = mpath+model+'-RCE_'+domain+'_'+temperature+'-2D.nc'
        elif model == 'UKMOi-vn11.0-CASIM' or model == 'UKMOi-vn11.0-RA1-T' or model == 'UKMOi-vn11.0-RA1-T-hrad' or model == 'UKMOi-vn11.0-RA1-T-nocloud':
            f = mpath+model+'_RCE_'+domain+temperature+'_2D.nc'
        elif model == 'UKMOi-vn11.0-CASIM' or model == 'UKMOi-vn11.0-RA1-T' or model == 'UKMOi-vn11.0-RA1-T-hrad' or model[0:7] == 'WRF_GCM':
            f = mpath+model+'_RCE_'+domain+temperature+'_2D.nc'
        elif model == 'WRF_COL_CRM':
            f = mpath+model+'_RCE_'+domain+temperature+'_2D.nc'
        elif model == 'WRF-CRM':
            f = mpath+'WRF_CRM_RCE_'+domain+temperature+'_2d.nc'
        elif model == 'MPAS':
            f = mpath+model+'_RCE_'+domain+temperature+'_2D_allvars_alltimes.nc'
        else:
            f = mpath+model+'-RCE_'+domain+temperature+'-2D.nc'

    # OPEN DATASET
    ds = xr.open_dataset(f, decode_times=False)

    # ADJUST VARIABLE NAME
    if model == 'UKMO-GA7.1':
        if variable == 'rlut':
            variable = 'toa_outgoing_longwave_flux'
        if variable == 'prw':
            variable = 'atmosphere_mass_content_of_water_vapor'
        if variable == 'sprw':
            variable = 'saturated_water_vapor_path'
        if variable == 'wa500':
            variable = 'vertical_velocity_500hpa'

    # OPEN VARIABLE
    if pmap == False:
        v = ds[variable]
        v = xr.DataArray(v.mean(dim=y)).values
        x = ds[x].values
        y = ds[y].values
    else:
        v = ds[variable].values
        if model == 'WRF-CRM' and domain == 'large':
            x = np.arange(0,2000)*3
            y = np.arange(0,133)*3
        else:
            x = ds[x].values
            y = ds[y].values

    # RAW DATA HAS NEGATIVE OLR DATA
    if model == 'WRF-CRM' and variable == 'rlut':
        v = abs(v)

    # PROCESS X-AXIS DATA
    if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'MESONH':
        if domain == 'small':
            lens = 1000
        if domain == 'large':
            lens = 3000
        x = np.arange(0,len(x)*lens,lens)
    if model == 'SCALE':
        if domain == 'large':
            x = (x*1000)-1500
        if domain == 'small':
            x = (x*1000)-500
    if model == 'UCLA-CRM':
        if domain == 'large':
            x += 2974500
        if domain == 'small':
            x += 47500
    if model == 'UKMOi-vn11.0-CASIM' or model == 'UKMOi-vn11.0-RA1-T' or model == 'UKMOi-vn11.0-RA1-T-hrad' or model == 'WRF_COL_CRM' or model == 'UKMOi-vn11.0-RA1-T-nocloud':
        if domain == 'small':
            x -= 500
        if domain == 'large':
            x -= 1500
    if model == 'WRF-CRM':
        x = x*1000
    if model [0:7] == 'WRF_GCM':
        x -= 25000
    if model == 'CM1':
        x -= 1500
    if model == 'FV3':
        x = (x-1)*3000
    if model == 'MicroHH':
        x = x-500
    if model == 'ICON_GCM':
        x[0] = 90-(180/129)
        for i in range(1,len(x)):
            x[i] = x[i-1]-(180/129)

    # PROCESS Y-AXIS DATA
    if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'MESONH':
        if domain == 'small':
            lens = 1000
        if domain == 'large':
            lens = 3000
        y = np.arange(0,len(y)*lens,lens)
    if model == 'SCALE':
        if domain == 'large':
            y = (y*1000)-1500
        if domain == 'small':
            y = (y*1000)-500
    if model == 'UCLA-CRM':
        if domain == 'large':
            y += 190500
        if domain == 'small':
            y += 47500
    if model == 'UKMOi-vn11.0-CASIM' or model == 'UKMOi-vn11.0-RA1-T' or model == 'UKMOi-vn11.0-RA1-T-hrad' or model == 'WRF_COL_CRM' or model == 'UKMOi-vn11.0-RA1-T-nocloud':
        if domain == 'small':
            y -= 500
        if domain == 'large':
            y -= 1500
    if model == 'WRF-CRM':
        y = y*1000
    if model [0:7] == 'WRF_GCM':
        y -= 25000
    if model == 'CM1':
        y -= 1500
    if model == 'FV3':
        y = (y-1)*3000
    if model == 'MicroHH':
        y = y-500

    # PROCESS TIME DATA
    ttt = 'time'
    if model == 'WRF_COL_CRM':
        ttt='days'
    t = ds[ttt].values
    if model == 'UCLA-CRM':
        t = t/86400.
    if model == 'GEOS_GCM':
        t=t+t[0]
    if model == 'CNRM-CM6-1':
        t=t-47116+(t[0]-47116)
    if model == 'UKMO-GA7.1':
        for i in range(len(t)):
            t[i] = i*(1/24)
    if model == 'MESONH':
        if domain =='large':
            t=(t/24)
            t=t+(1/24)
    if model == 'WRF_COL_CRM' and temperature == '295' and domain == 'large':
        for i in range(len(t)):
            t[i] = (i+1)/24
    if model == 'WRF-CRM' and domain == 'small':
        t = t/24
    if model == 'IPSL-CM6':
        if temperature == '300':
            t = (t+40800)/86400
        else:
            t = (t+43200)/86400
    if model == 'MicroHH':
        t = t/3600/24

    # CLOSE DATASET
    ds.close()

    # LAST TIME STEP IS CORRUPT
    if model == 'UCLA-CRM' and temperature == '295':
        t = t[:-1]
        v = v[:-1]

    return(v,x,y,t)

def process(model, domain, temperature, demension, variable, mfiles, th, p='0'):
    """
        Processes

        Args:
            model: string, which model is being processed
                must be format in the directory system
            domain: string, which domain is being processed
            temperature: string, which SST is being processed
            demension:
            variable: string, which variable is being processed
            mfiles: boolean, False for all variables and times are in one file
            th:
            p: (optional, '0')  ,

        Returns:
            height:
            var:
            vavg:
    """

    # ADJUST VARIABLE NAME IMPACTING FILE NAME
    if variable == 'sprw_avg':
        if model == 'ECHAM6_GCM' or model == 'NICAM' or model == 'SP-CAM' or model == 'SPX-CAM':
            variable = 'spwr_avg'
    if model == 'UKMO-GA7.1':
        if variable == 'pa_avg':
            variable = 'plevrho_avg'

    # MODEL PATH
    rcemip = '/huracan/tank2/columbia/RCEMIP/'
    if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'ICON_GCM':
        mpath  = rcemip+model+'/'+'RCE_'+domain+'_'+temperature+'/'+demension+'/'
    elif model[0:7] == 'WRF_GCM':
        mpath  = rcemip+'WRF_GCM/'+model[8:12]+'/RCE_'+domain+temperature+'/'+demension+'/'
    else:
        mpath  = rcemip+model+'/'+'RCE_'+domain+temperature+'/'+demension+'/'

    # FILE PATH
    if mfiles == True:
        if model == 'SAM6.11.2':
            f = rcemip+model+'/RCEMIP_upload/RCE_'+domain+temperature+'/'+demension+'/SAM_CRM_RCE_'+domain+temperature+'_'+demension+'_'+variable+'.nc'
        elif model == 'SAM0-UNICON':
            f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'_0003.nc'
        else:
            f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'.nc'
    if variable == 'pa_avg':
        if model == 'SP-CAM' or model == 'SPX-CAM':
            f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'.nc'
        if model == 'SAM_GCRM':
            f = '/huracan/tank2/columbia/RCEMIP/SAM_GCRM/RCE_large300/1D/SAM_GCRM_RCE_large300_1D_cldfrac_avg.nc'
        if model == 'SAM6.11.2':
            f = rcemip+model+'/RCEMIP_upload/RCE_'+domain+temperature+'/'+demension+'/SAM_CRM_RCE_'+domain+temperature+'_'+demension+'_cldfrac_avg.nc'
    if mfiles == False:
        if model == 'CM1' or model == 'MPAS':
            f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_allvars_alltimes.nc'
        elif model == 'ECHAM6_GCM':
            f = mpath+model+'-RCE_'+domain+temperature+'-'+demension+'.nc'
        elif model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'ICON_GCM':
            f = mpath+model+'-RCE_'+domain+'_'+temperature+'-'+demension+'.nc'
        elif model == 'WRF_COL_CRM':
            f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'.nc'
        elif model == 'WRF-CRM':
            f = mpath+'WRF_CRM_RCE_'+domain+temperature+'_'+demension[0]+'d.nc'
        else:
            f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'.nc'
    if variable == 'hur_avg' and demension == '1D':
        if model == 'WRF-CRM':
            th = 'zg_avg'
            f = mpath+'WRF_CRM_RCE_'+domain+temperature+'_1d_newrh.nc'
        if model == 'WRF_COL_CRM' or model == 'IPSL-CM6' or model[:7] == 'WRF_GCM':
            if model[:7] != 'WRF_GCM':
                th = 'zg_avg'
            f = mpath+model+'_RCE_'+domain+temperature+'_1D_newrh.nc'
        if model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM':
            f = mpath+model+'-RCE_'+domain+'_'+temperature+'-3D_last25d_hur_satiw_ice_fldmean.nc'

    # ADJUST VARIABLE NAME
    if variable == 'pa_avg':
        if model == 'ICON_GCM' or model[:7] == 'WRF_GCM':
            if model[:7] == 'WRF_GCM':
                p='p_avg'
            variable = 'p_avg'
        if model == 'SAM_GCRM' or model == 'SAM6.11.2':
            variable = 'p'
            p='p'
        if model == 'ICON_LEM_CRM':
            variable = 'pres_avg'
        if model == 'FV3':
            variable = 'pfull'
            f = mpath+'FV3_RCE_large'+temperature+'_1D_zg_avg.nc'
        if model == 'WRF-CRM':
            if domain == 'large':
                variable = 'Pressure'
                p='Pressure'
            if domain == 'small':
                variable = 'pressure'
                p='pressure'
        if model == 'IPSL-CM6':
            variable = 'plev'
            p = 'plev'
        if model == 'MicroHH':
            variable = 'phydro'
    if model == 'UKMO-GA7.1':
        if variable == 'ta_avg':
            variable = 'air_temperature'
        if variable == 'ua_avg':
            variable ='eastward_wind'
        if variable == 'va_avg':
            variable ='northward_wind'
        if variable == 'hus_avg':
            variable ='specific_humidity'
        if variable == 'hur_avg':
            variable = 'relative_humidity'
        if variable == 'clw_avg':
            if domain =='large':
                variable ='mass_fraction_of_cloud_liquid_water_in_air'
            if domain =='small':
                variable ='mass_fraction_of_cloud_liquid_water'
        if variable == 'cli_avg':
            if domain == 'large':
                variable = 'mass_fraction_of_cloud_ice_in_air'
            if domain == 'small':
                variable = 'mass_fraction_of_cloud_ice'
        if variable == 'pr_avg':
            variable = 'precipitation_flux'
        if variable == 'plw_avg':
            if domain == 'large':
                variable ='mass_fraction_of_precipitating_liquid_water_in_air'
            if domain == 'small':
                variable ='mass_fraction_of_precipitating_liquid_water'
        if variable == 'theta_avg':
            if domain == 'large':
                variable ='air_potential_temperature'
            if domain == 'small':
                variable ='potential_temperature'
        if variable == 'thetae_avg':
            variable ='equivalent_potential_temperature'
        if variable == 'tntrs_avg':
            if domain == 'large':
                variable = 'tendency_of_air_temperature_due_to_shortwave_heating'
            if domain == 'small':
                variable ='shortwave_radiative_heating_rate'
        if variable == 'tntrl_avg':
            if domain == 'large':
                variable ='tendency_of_air_temperature_due_to_longwave_heating'
            if domain == 'small':
                variable ='longwave_radiative_heating_rate'
        if variable == 'tntrscs_avg':
            if domain == 'large':
                variable = 'tendency_of_air_temperature_due_to_shortwave_heating_assuming_clear_sky'
            if domain == 'small':
                variable ='shortwave_radiative_heating_rate_assuming_clear_sky'
        if variable == 'tntrlcs_avg':
            if domain == 'large':
                variable = 'tendency_of_air_temperature_due_to_longwave_heating_assuming_clear_sky'
            if domain == 'small':
                variable ='longwave_radiative_heating_rate_assuming_clear_sky'
        if variable == 'cldfrac_avg':
            variable = 'cloud_fraction'
        if variable == 'plevrho_avg':
            variable = 'air_pressure'
        if variable == 'hfls_avg':
            variable = 'surface_upward_latent_heat_flux'
        if variable == 'hfss_avg':
            variable = 'surface_upward_sensible_heat_flux'
        if variable == 'clwvi_avg':
            if domain == 'small':
                variable = 'condensed_water_path'
            if domain == 'large':
                variable = 'atmosphere_mass_content_of_cloud_condensed_water'
        if variable == 'clivi_avg':
            if domain == 'small':
                variable = 'ice_water_path'
            if domain == 'large':
                variable = 'atmosphere_mass_content_of_cloud_ice'
        if variable == 'rlds_avg':
            if domain == 'small':
                variable='surface_downwelling_longwave_flux'
            if domain == 'large':
                variable='surface_downwelling_longwave_flux_in_air'
        if variable == 'rlus_avg':
            if domain == 'small':
                variable='surface_upwelling_longwave_flux'
            if domain == 'large':
                variable = 'surface_upwelling_longwave_flux_in_air'
        if variable == 'rsds_avg':
            if domain == 'small':
                variable='surface_downwelling_shortwave_flux'
            if domain == 'large':
                variable = 'surface_downwelling_shortwave_flux_in_air'
        if variable == 'rsus_avg':
            if domain == 'small':
                variable='surface_upwelling_shortwave_flux'
            if domain == 'large':
                variable = 'surface_upwelling_shortwave_flux_in_air'
        if variable == 'rsdscs_avg':
            if domain == 'small':
                variable='surface_downwelling_shortwave_flux_assuming_clear_sky'
            if domain == 'large':
                variable = 'surface_downwelling_shortwave_flux_in_air_assuming_clear_sky'
        if variable =='rsuscs_avg':
            if domain == 'small':
                variable='surface_downwelling_shortwave_flux_assuming_clear_sky'
            if domain == 'large':
                variable='surface_upwelling_shortwave_flux_in_air_assuming_clear_sky'
        if variable =='rldscs_avg':
            if domain == 'small':
                variable='surface_downwelling_longwave_flux_assuming_clear_sky'
            if domain == 'large':
                variable = 'surface_downwelling_longwave_flux_in_air_assuming_clear_sky'
        if variable == 'rluscs_avg':
            if domain == 'small':
                variable='surface_upwelling_longwave_flux_assuming_clear_sky'
            if domain == 'large':
                variable = 'surface_upwelling_longwave_flux_in_air_assuming_clear_sky'
        if variable == 'rsdt_avg':
            variable='toa_incoming_shortwave_flux'
        if variable == 'rsut_avg':
            variable='toa_outgoing_shortwave_flux'
        if variable == 'rlut_avg':
            variable='toa_outgoing_longwave_flux'
        if variable == 'rsutcs_avg':
            variable='toa_outgoing_shortwave_flux_assuming_clear_sky'
        if variable == 'rlutcs_avg':
            variable='toa_outgoing_longwave_flux_assuming_clear_sky'
        if variable == 'prw_avg':
            variable = 'atmosphere_mass_content_of_water_vapor'
        if variable == 'sprw_avg':
            variable = 'saturated_water_vapor_path'
    if model == 'CNRM-CM6-1' and demension == '0D' and domain == 'small':
        variable = variable[:-4]

    # TIME NAME
    if model == 'WRF_COL_CRM':
        if variable == 'hur_avg':
            ttt = 'Time'
            th = 'bottom_top'
        else:
            ttt = 'days'
    else:
        ttt = 'time'

    # OPEN DATASET, TIME DATA, AND VARIABLE DATA
    if model == 'SAM0-UNICON': # COMBINE DATA FROM ACROSS FOUR TIME-SEPARATED FILES

        d1 = xr.open_dataset(mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'_0001.nc',decode_times=False)
        v1 = d1[variable]
        d1.close()

        d2 = xr.open_dataset(mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'_0002.nc',decode_times=False)
        v2 = d2[variable]
        d2.close()

        d3 = xr.open_dataset(mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'_0003.nc',decode_times=False)
        v3 = d3[variable]
        d3.close()

        d4 = xr.open_dataset(mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_'+variable+'_0004.nc',decode_times=False)
        v4 = d4[variable]
        d4.close()

        var = xr.concat([v1,v2,v3,v4],dim=ttt)

        time = np.arange(0,np.shape(var)[0])/24

        if demension == '1D':
            dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_1D_zg_avg_0001.nc',decode_times=False)
            h1 = dz['zg_avg']
            dz.close()
            dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_1D_zg_avg_0002.nc',decode_times=False)
            h2 = dz['zg_avg']
            dz.close()
            dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_1D_zg_avg_0003.nc',decode_times=False)
            h3 = dz['zg_avg']
            dz.close()
            dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_1D_zg_avg_0004.nc',decode_times=False)
            h4 = dz['zg_avg']
            dz.close()
            height = xr.concat([h1,h2,h3,h4],dim=ttt)
    elif model == 'GEOS_GCM' and variable == 'pa_avg':
        ds = xr.open_dataset(f, decode_times=False)
        var  = ds[variable]
        p = 'pa_avg'
        time = [0]
    elif variable == 'hur_avg' and model[:4] == 'ICON' and model != 'ICON_GCM':
        ds = xr.open_dataset(f, decode_times=False)

        time = ds[ttt].values
        var  = ds['hur']
    else:
        ds = xr.open_dataset(f, decode_times=False)

        time = ds[ttt].values
        var  = ds[variable]

    # PROCESS TIME DATA
    if model == 'UCLA-CRM':
        time = time/86400.
    if model == 'UKMO-GA7.1':
        for i in range(len(time)):
            time[i] = i*(1/24)
    if model == 'MESONH':
        if domain =='large':
            time=(time/24)
            time=time+(1/24)
    if model == 'IPSL-CM6':
        if temperature == '300':
            time = (time+40800)/86400
        else:
            time = (time+43200)/86400

    # 75.04 TIME INDEX FOR AVERAGING
    if time[0] == 0:
        tavg = 1801
    else:
        tavg = 1800

    # PROCESS 0D DATA
    if demension == '0D':
        # PROCESS VARIABLE DATA
        if len(var) > 1:
            var = xr.DataArray.squeeze(var)

        if variable[:2] == 'rl' or variable[:2] == 'rs':
            var = abs(var) # MAKE ALL RADIATIVE FLUXES POSITIVE
        if variable == 'pr_avg' or variable == 'pr' or variable == 'precipitation_flux':
            var = var * 86400 # CONVERT PRECIP UNITS FROM kg/m^2/s TO mm/day
        if variable == 'hfls_avg' or variable == 'hfss_avg':
            var = np.abs(var) # MAKE ALL SURFACE FLUXES POSITIVE

        # SOME MODELS LABELD TOTAL CLOUD WATER AS JUST CLOUD LIQUID WATER
        if variable == 'clwvi_avg':
            if model[:2] == 'SP' or model[:4] == 'ICON' or model == 'ECHAM6_GCM' or model == 'GEOS_GCM' or model[:7] == 'WRF_GCM':
                if mfiles == True:
                    fw = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_clwvi_avg.nc'
                    fi = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'_clivi_avg.nc'
                    vw = xr.open_dataset(fw,decode_times=False)['clwvi_avg']
                    vi = xr.open_dataset(fi,decode_times=False)['clivi_avg']
                if mfiles == False:
                    if model == 'ECHAM6_GCM':
                        f = mpath+model+'-RCE_'+domain+temperature+'-'+demension+'.nc'
                    elif model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM' or model == 'ICON_GCM':
                        f = mpath+model+'-RCE_'+domain+'_'+temperature+'-'+demension+'.nc'
                    else:
                        f = mpath+model+'_RCE_'+domain+temperature+'_'+demension+'.nc'
                    vw = xr.open_dataset(f,decode_times=False)['clwvi_avg']
                    vi = xr.open_dataset(f,decode_times=False)['clivi_avg']
                if model == 'ECHAM6_GCM' or model[:4] == 'ICON':
                    vw = xr.DataArray.squeeze(vw)
                    vi = xr.DataArray.squeeze(vi)
                var = vw+vi
            if model == 'MESONH':
                cwp,__,__,__,__,__,__,__ = process_2D(model, domain, temperature, 'clwvi',True, 'CRM')
                var = np.zeros((np.shape(cwp)[0]))
                for j in range(len(var)):
                    var[j] = np.mean(cwp[j])
                var = xr.DataArray(var)
                vavg = xr.DataArray(var[tavg:].mean()).values
                var = var.values
            # OTHER NOTES ON TOTAL WATER ERRORS:
            # CM1 subtract off rain but they are not variables or just use it and
            #   make a comment on how it is not right
            # UCLA also added grapel, but that is small and no easy way to get rid of
            #   but if it is radiatively active it might be relevent to add anyway

        # AVERAGE DATA OVER ALL BUT FIRST 75 DAYS (STARTS AT DAY 75.04)
        if variable == 'clwvi_avg' and model == 'MESONH': # ALREADY AVERAGED DATA
            vavg = vavg
            var = var
        elif model == 'FV3': # ONLY ONE DAY
            vavg = var.values[0]
            var = var.values[0]
        elif model == 'IPSL-CM6': # DAILY, RATHER THAN HOURLY, AVERAGES
            vavg = xr.DataArray(var[75:].mean(dim=ttt)).values
            var = var.values
        else:
            vavg = xr.DataArray(var[tavg:].mean(dim=ttt)).values
            var = var.values

        # CLOSE DATASET
        if model != 'SAM0-UNICON':
            ds.close()

        return(np.squeeze(time),np.squeeze(var),np.squeeze(vavg))

    # PROCESS 1D DATA
    if demension == '1D':
        # OPEN HEIGHT DATA
        if model == 'IPSL-CM6' or model == 'FV3' or model == 'CNRM-CM6-1' or model == 'GEOS_GCM' or model == 'SP-CAM' or model == 'SPX-CAM' or model == 'UKMO-GA7.1' or model == 'CAM5_GCM' or model == 'CAM6_GCM':
            if model == 'IPSL-CM6' or model == 'FV3' or model == 'CNRM-CM6-1' or model == 'GEOS_GCM' or model == 'CAM5_GCM' or model == 'CAM6_GCM':
                if model == 'GEOS_GCM':
                    if variable !=' pa_avg':
                        dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_'+demension+'_zg_avg.nc',decode_times=False)
                else:
                    dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_'+demension+'_zg_avg.nc',decode_times=False)
            if model == 'UKMO-GA7.1':
                if domain =='large':
                    dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/UKMO-GA7.1/RCE_'+domain+temperature+'/1D/UKMO-GA7.1_RCE_'+domain+temperature+'_1D_height_rho.nc',decode_times=False)
                if  domain =='small':
                    dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/UKMO-GA7.1/RCE_'+domain+temperature+'/1D/UKMO-GA7.1_RCE_'+domain+temperature+'_1D_height_rho_avg.nc',decode_times=False)
            if model == 'SP-CAM' or model == 'SPX-CAM':
                dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/'+model+'_RCE_'+domain+temperature+'_1D_z_avg.nc',decode_times=False)
            if model == 'GEOS_GCM':
                if variable !=' pa_avg':
                    height = dz[th]
            else:
                height = dz[th]
        elif model == 'WRF-CRM' and variable != 'hur_avg':
            dz = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/'+model+'/RCE_'+domain+temperature+'/1D/WRF_CRM_RCE_1d_height.nc',decode_times=False)
            height = dz['zg_avg']
        elif variable == 'hur_avg' and model[:4] == 'ICON' and model != 'ICON_GCM':
            height = f = xr.open_dataset(mpath+model+'-RCE_'+domain+'_'+temperature+'-'+demension+'.nc')[th]
        elif model[:7] == 'WRF_GCM' and variable == 'hur_avg':
            height = xr.open_dataset(mpath+model+'_RCE_'+domain+temperature+'_1D.nc')['h_avg']
        elif model[:7] == 'WRF_COL' and variable == 'hur_avg':
            height = xr.open_dataset(mpath+model+'_RCE_'+domain+temperature+'_1D.nc')['zg_avg']
        else:
            if model != 'SAM0-UNICON':
                height = ds[th]

        # PROCESS VARIABLE AND HEIGHT DATA
        if len(var) > 1:
            var = xr.DataArray.squeeze(var)
            height = xr.DataArray.squeeze(height)
        # if model != 'GEOS_GCM' and variable != 'pa_avg':
        #     height = xr.DataArray.squeeze(height)
        if  model == 'MPAS':
            var    = xr.DataArray.transpose(var)
            height = xr.DataArray.transpose(height)
        if model == 'IPSL-CM6':
            height = xr.DataArray(height[75:].mean(dim=ttt))
        if model == 'CAM5_GCM' or model == 'CAM6_GCM' or model == 'ECHAM6_GCM' or model == 'CNRM-CM6-1' or model == 'SAM0-UNICON':
            height = xr.DataArray(height[tavg:].mean(dim=ttt))
        if model == 'UKMO-GA7.1' and domain == 'small':
            height = xr.DataArray(height[tavg:].mean(dim=ttt))
        # if model == 'WRF-CRM' and domain == 'small' and variable != 'hur_avg':
        #     height = xr.DataArray(height[tavg:].mean(dim=ttt))
        if model == 'ICON_LEM_CRM' and variable != 'pres_avg':
            var = var.where(var < 10000)
        if variable == 'cldfrac_avg': # MAKE UNITLESS
            if model == 'NICAM' or model == 'CNRM-CM6-1':
                var = var/100
        if variable == 'hur_avg': # MAKE UNIT PERCENT
            if model == 'dam' or model == 'GEOS_GCM' or model == 'ICON_GCM' or model == 'FV3' or model == 'IPSL-CM6':
                var = var*100
            if model == 'CNRM-CM6-1' and domain == 'large':
                var = var*100
            if model[:7] == 'WRF_GCM' or model == 'WRF_COL_CRM':
                var = var*100
        if variable == 'hur': # MAKE UNIT PERCENT
            var = var*100
        if variable == 'relative_humidity': # MAKE UNIT PERCENT
            if model == 'UKMO-GA7.1' and domain =='small':
                var = var*100
        if variable == 'cloud_fraction': # MAKE UNITLESS
            if model == 'UKMO-GA7.1' and domain =='large':
                var = var/100

        # AVERAGE DATA OVER ALL BUT FIRST 75 DAYS (STARTS AT DAY 75.04)
        if model == 'SP-CAM' and variable =='cldfrac_avg':
            vavg = var[len(time)-1]
        elif model == 'SPX-CAM' and variable =='cldfrac_avg':
            vavg = var[len(time)-1]
        elif model == 'FV3':
            vavg = var
            var = var.values
        elif model == 'IPSL-CM6' and p == '0':
            vavg = xr.DataArray(var[75:].mean(dim=ttt))
            var = var.values
        elif p!='0':
            vavg = ds[p]
        else:
            vavg = xr.DataArray(var[tavg:].mean(dim=ttt))
        if variable == 'hur_avg':
            if model[:7] == 'WRF_GCM':
                vavg = xr.DataArray(var[np.shape(var)[0]-100:].mean(dim=ttt))
            if model == 'WRF_COL_CRM' or model == 'ICON_LEM_CRM' or model == 'ICON_NWP_CRM':
                vavg = xr.DataArray(var[:,:].mean(dim=ttt))
        if model == 'WRF-CRM' and variable == 'pressure':
            vavg = xr.DataArray(var[tavg:].mean(dim=ttt))
           
        # FURTHER ADJUST AND FINALIZE DATA ARRAYS
        if variable == 'hus_avg' or variable == 'clw_avg' or variable == 'cli_avg' or variable == 'plw_avg' or variable == 'pli_avg':
            # MAKE UNITS g/g to g/kg
            vavg = vavg*1000
            var = var*1000
        if variable =='mass_fraction_of_cloud_liquid_water_in_air' or variable =='mass_fraction_of_cloud_liquid_water' or variable == 'mass_fraction_of_cloud_ice_in_air' or variable == 'mass_fraction_of_cloud_ice':
            # MAKE UNITS g/g to g/kg
            vavg = vavg*1000
            var = var*1000

        if variable == 'tntrs_avg' or variable == 'tntrl_avg' or variable == 'tntrscs_avg' or variable == 'tntrlcs_avg' or variable == 'tendency_of_air_temperature_due_to_shortwave_heating'  or variable == 'shortwave_radiative_heating_rate' or variable == 'tendency_of_air_temperature_due_to_longwave_heating' or variable == 'longwave_radiative_heating_rate' or variable == 'tendency_of_air_temperature_due_to_shortwave_heating_assuming_clear_sky' or variable == 'shortwave_radiative_heating_rate_assuming_clear_sky' or variable == 'tendency_of_air_temperature_due_to_longwave_heating_assuming_clear_sky' or variable =='longwave_radiative_heating_rate_assuming_clear_sky':
            # MAKE UNITS K/s to K/day
            vavg = vavg*84600
            var = var * 84600

        if model != 'GEOS_GCM' and variable != 'pa_avg':
            height = height.values

        vavg = vavg.values

        if model == 'ICON_NWP_CRM' or model == 'ICON_LEM_CRM' or model[0:3] == 'CAM' or model == 'ECHAM6_GCM' or model == 'GEOS_GCM' or model == 'ICON_GCM' or model == 'SAM0-UNICON' or model[0:2] == 'SP':
            if model != 'GEOS_GCM' and variable != 'pa_avg':
                height = np.flip(height)
                vavg = np.flip(vavg)
        if model == 'CNRM-CM6-1' and domain == 'small':
            height = np.flip(height)
            vavg = np.flip(vavg)

        # CLOSE DATASET
        if model != 'SAM0-UNICON':
            ds.close()

        return(np.squeeze(height),np.squeeze(var),np.squeeze(vavg))

def pressure(model,domain,temperture):
    """
        Processes

        Args:
            model: string, which model is being processed
                must be format in the directory system
            domain: string, which domain is being processed
            temperature: string, which SST is being processed

        Returns:
            pavg:
    """

    if model == 'NICAM':
        ds = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/NICAM/RCE_'+domain+temperture+'/1D/NICAM_RCE_'+domain+temperture+'_1D_pa_avg.nc', decode_times=False)

        p = ds['pa_avg']
        t = ds['time']
        h = ds['z']
        p = xr.DataArray.squeeze(p)

        pavg = xr.DataArray(p.mean(dim='time')) # last 25 days of pressure values

    if model == 'SCALE':
        ds = xr.open_dataset('/huracan/tank2/columbia/RCEMIP/SCALE/RCE_'+domain+temperture+'/1D/SCALE_RCE_'+domain+temperture+'_1D_pa_avg.nc', decode_times=False)

        p = ds['pa_avg']
        t = ds['time']
        h = ds['lev']
        p = xr.DataArray.squeeze(p)

        pavg = xr.DataArray(p[(len(t)-100):].mean(dim='time')) # every 15 minutes

    ds.close()
    return(pavg.values)

def processLES(model, version, temperature, demension, variable, mfiles, th):
    """
        Processes

        Args:
            model: string, which model is being processed
                must be format in the directory system
            version:
            temperature: string, which SST is being processed
            demension:
            variable: string, which variable is being processed
            mfiles: boolean, False for all variables and times are in one file
            th:

        Returns:
            0D or 1D:
                height:
                var:
                vavg:
            2D:
                v: 3D array [time,x,y], the variable processed
                x: 1D array [x], zonal data (meters or degrees)
                y: 1D array [x], meridional data (meters or degrees)
                t: 1D array [t], time data (days)
    """

    rcemip = '/huracan/tank2/columbia/RCEMIP/'
    domain = 'small'

    if variable == 'pa_avg' and model == 'SAM_CRM':
        variable = 'p'

    # MODEL PATH
    if model == 'ICON_LEM_CRM':
        mpath  = rcemip+model+'/'+'RCE_small_'+version+'_'+temperature+'/'+demension+'/'
    else:
        mpath  = rcemip+model+'/'+'RCE_small_'+version+temperature+'/'+demension+'/'

    # FILE PATH
    if mfiles == True:
        f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_'+variable+'.nc'
    if mfiles == False:
        if model == 'MicroHH':
            if variable == 'pa_avg':
                f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_pa_avg.nc'
                variable = 'phydro'
            else:
                f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'.nc'
        elif model == 'CM1':
            f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_allvars_alltimes.nc'
        else:
            if variable == 'sprw' and model[:4] == 'ICON':
                f = mpath+model+'-RCE_small_'+version+'_'+temperature+'-2D_sprw_last25d.nc'
            else:
                f = mpath+model+'-RCE_small_'+version+'_'+temperature+'-'+demension+'.nc'
    if variable == 'hur_avg' and model[:4] == 'ICON':
        f = mpath+'ICON_LEM_CRM-RCE_small_'+version+'_'+temperature+'-3D_last25d_hur_satiw_ice_fldmean.nc'

    # OPEN DATASET, TIME DATA, AND VARIABLE DATA
    ds = xr.open_dataset(f, decode_times=False)
    ttt  = 'time'
    if variable != 'p':
        time = ds[ttt].values
    else:
        time = xr.open_dataset(mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_cldfrac_avg.nc', decode_times=False)['time'].values
    if variable == 'pa_avg' and model[:4] == 'ICON':
        variable = 'pres_avg'

    if variable == 'hur_avg' and model[:4] == 'ICON':
        var  = ds['hur']
    else:
        var  = ds[variable]

    # LIMIT LES DATA TO FIRST 50 DAYS
    if model == 'MESONH' and version == 'les':
        time = ds[ttt][0:1200].values
        var  = ds[variable][0:1200]

    # PROCESS TIME DATA
    if model[:5] == 'DALES': # RAW TIME DATA IS NOT GOOD
        if version == 'vert':
            time = np.arange((1/24),(100+(1/24)),(1/24))
        if version == 'les':
            time = np.arange((1/24),(50+(1/24)),(1/24))
    if model[:7] == 'MicroHH': # MAKE UNITS TO DAYS
        time = time/3600/24

    # INDECIES FOR AVERAGING START AND END (75.04-end FOR VERT 25.04-50.0 FOR LES)
    if version == 'vert':
        if time[0] == 0:
            tavg_b = 1801
            tavg_e = np.shape(time)[0]
        if time[0] != 0:
            tavg_b = 1800
            tavg_e = np.shape(time)[0]
    if version == 'les':
        if time[0] == 0:
            tavg_b = 601
            tavg_e = 1202
        if time[0] != 0:
            tavg_b = 600
            tavg_e = 1201

    # PROCESS 0D DATA
    if demension == '0D':
        var = xr.DataArray.squeeze(var)
        if variable[:2] == 'rl' or variable[:2] == 'rs':
            var = abs(var) # MAKE RADIATIVE FLUXES POSITIVE
        if variable == 'pr_avg' or variable == 'pr' or variable == 'precipitation_flux':
            var = var * 86400 # MAKE PRECIP UNITS mm/day

        # SOME MODELS LABELD TOTAL CLOUD WATER AS JUST CLOUD LIQUID WATER
        if variable == 'clwvi_avg':
            if model == 'MicroHH' or model == 'SAM_CRM':
                if mfiles == True:
                    fw = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_clwvi_avg.nc'
                    fi = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_clivi_avg.nc'
                    vw = xr.open_dataset(fw,decode_times=False)['clwvi_avg']
                    vi = xr.open_dataset(fi,decode_times=False)['clivi_avg']
                if mfiles == False:
                    if model == 'MicroHH':
                        if variable == 'pa_avg':
                            f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_pa_avg.nc'
                            variable = 'phydro'
                        else:
                            f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'.nc'
                    elif model == 'CM1':
                        f = mpath+model+'_RCE_small_'+version+temperature+'_'+demension+'_allvars_alltimes.nc'
                    else:
                        f = mpath+model+'-RCE_small_'+version+'_'+temperature+'-'+demension+'.nc'
                    vw = xr.open_dataset(f,decode_times=False)['clwvi_avg']
                    vi = xr.open_dataset(f,decode_times=False)['clivi_avg']
                if model == 'ECHAM6_GCM' or model[:4] == 'ICON':
                    vw = xr.DataArray.squeeze(vw)
                    vi = xr.DataArray.squeeze(vi)
                var = vw+vi
            if model == 'MESONH':
                cwp,__,__,__,__,__,__,__ = processLES(model, version, temperature, '2D', 'clwvi', mfiles, th)
                var = np.zeros((np.shape(cwp)[0]))
                for j in range(len(var)):
                    var[j] = np.mean(cwp[j])
                var = xr.DataArray(var)
                vavg = xr.DataArray(var[tavg_b:tavg_e].mean()).values
                var = var.values
            # OTHER NOTES ON TOTAL WATER ERRORS:
            # CM1 subtract off rain but they are not variables or just use it and
            #   make a comment on how it is not right
            # UCLA also added grapel, but that is small and no easy way to get rid of
            #   but if it is radiatively active it might be relevent to add anyway

        # TIME-AVERAGE DATA
        if variable == 'clwvi_avg' and model == 'MESONH':
            vavg = vavg
            var = var
        else:
            vavg = xr.DataArray(var[tavg_b:tavg_e].mean(dim=ttt)).values
            var = var.values

        # CLOSE DATASET
        ds.close()

        return(time,var,vavg)

    # PROCESS 1D DATA
    if demension == '1D':
        # OPEN HEIGHT DATA
        if variable == 'hur_avg' and model[:4] == 'ICON':
            height = xr.open_dataset(mpath+model+'-RCE_small_'+version+'_'+temperature+'-'+demension+'.nc')[th]
        else:
            height = ds[th]

        # PROCESS DATA
        var    = xr.DataArray.squeeze(var)
        height = xr.DataArray.squeeze(height)

        # TIME-AVERAGE DATA
        if model == 'SAM_CRM' and variable == 'p':
            vavg = var
        elif model[:5] == 'DALES':
            var=var.values
            vavg=np.mean(var[tavg_b:tavg_e,:],axis=0)
        else:
            vavg = xr.DataArray(var[tavg_b:tavg_e].mean(dim=ttt)).values

        if variable == 'hur_avg' and model[:4] == 'ICON':
            vavg = xr.DataArray(var[:,:].mean(dim=ttt))

        # ADJUST UNITS
        if variable == 'hus_avg' or variable == 'clw_avg' or variable == 'cli_avg' or variable == 'plw_avg' or variable == 'pli_avg':
            if variable == 'clw_avg' or variable == 'cli_avg': # UNITS FROM g/g TO g/kg
                if model[:5] != 'DALES':
                    vavg = vavg*1000
                    var = var*1000
                if model[:5] == 'DALES':
                    if version == 'les' and temperature != '300':
                        vavg = vavg*1000
                        var = var*1000
                    else:
                        vavg = vavg/1000
                        var = var/1000
            else:
                vavg = vavg*1000
                var = var*1000
        if variable[:4] == 'tntr':
            vavg = vavg*84600 # UNITS FROM K/s TO K/day
            var = var*84600

        # FINALIZE DATA
        if model[:5] != 'DALES':
            var = var.values
        height = height.values

        if model == 'ICON_LEM_CRM':
            height = np.flip(height)
            vavg = np.flip(vavg)

        # CLOSE DATA
        ds.close()

        return(height,var,vavg)

    # PROCESS 2D DATA
    if demension == '2D':
        # AXIS VARIABLE NAME
        if model == 'ICON_LEM_CRM':
            x = 'lon'
            y = 'lat'
        elif model[:5] == 'DALES':
            if version == 'les' or model == 'DALES_damping_rad':
                x = 'xt'
                y = 'yt'
            else:
                x = 'xm'
                y = 'ym'
        else:
            x = 'x'
            y = 'y'

        # OPEN DATASET
        ds = xr.open_dataset(f, decode_times=False)

        # OPEN AXIS DATA
        x = ds[x].values
        y = ds[y].values

        # PROCESS AXIS DATA
        if model == 'MESONH':
            if version == 'vert':
                x=(x-1)*1000
                y=(y-1)*1000
            if version == 'les':
                x=(x-0.2)*1000
                y=(y-0.2)*1000
        if model == 'ICON_LEM_CRM':
            if version == 'les':
                lens = 200
                x = (np.arange(0,len(x)*lens,lens))
                y = (np.arange(0,len(y)*lens,lens))
            if version == 'vert':
                lens = 1000
                x = (np.arange(0,len(x)*lens,lens))
                y = (np.arange(0,len(y)*lens,lens))
        if model == 'MicroHH':
            if version == 'vert':
                x=x-500
                y=y-500
            if version == 'les':
                x=x-100
                y=y-100
        if model[:5] == 'DALES' and version == 'les':
            x=x-100
            y=y-100
        if model == 'DALES_damping_rad':
            x=x-500
            y=y-500

        # PROCESS TIME AND VARIABLE DATA
        t = time
        v = var.values

        if model == 'MicroHH':
            v = np.squeeze(v)

        # CLOSE DATASET
        ds.close()

        return(v,x,y,t)

def process_CM12D(model, domain, temperature, variable, mfiles,mtype,cmt):
    """
        Processes 2D data for all but LES/VER models

        Args:
            model: string, which model is being processed
                must be format in the directory system
            domain: string, which domain is being processed
            temperature: string, which SST is being processed
            variable: string, which variable is being processed
            mfiles: boolean, False for all variables and times are in one file
            mtype: string, denotes global or cartesian plane
            cmt: (optional, True) boolean,

        Returns:
            v: 3D array [time,x,y], the variable processed
            x: 1D array [x], zonal data (meters or degrees)
            y: 1D array [x], meridional data (meters or degrees)
            t: 1D array [t], time data (days)
    """

    # AXIS NAMES
    x = 'x'
    y = 'y'

    # FILE PATH
    rcemip = '/huracan/tank2/columbia/RCEMIP/'
    mpath  = rcemip+model+'/'+'RCE_'+domain+temperature+'/2D/'
    if mtype == 'les' or mtype == 'vert':
        mpath  = rcemip+model+'/RCE_small_'+mtype+temperature+'/2D/'
        f = mpath+model+'_RCE_small_'+mtype+temperature+'_2D_allvars_hour'+cmt+'.nc'
    else:
        mpath  = rcemip+model+'/'+'RCE_'+domain+temperature+'/2D/'
        f = mpath+model+'_RCE_'+domain+temperature+'_2D_allvars_hour'+cmt+'.nc'

    # OPEN DATASET, VARIABLE DATA, X-AXIS DATA, AND Y-AXIS DATA
    ds = xr.open_dataset(f, decode_times=False)

    v = ds[variable].values
    x = ds[x].values
    y = ds[y].values

    # PROCESS AXIS DATA
    if mtype == 'les':
        x-=100
        y-=100
    else:
        if domain == 'large':
            x-=1500
            y-=1500
        if domain == 'small' or mtype == 'vert':
            x-=500
            y-=500

    # OPEN TIME DATA
    ttt = 'time'
    t = ds[ttt].values

    # CLOSE DATASET
    ds.close()

    return(v,x,y,t)

def process_NICAM2D(model, domain, temperature, variable, mfiles,mtype,cmt):
    """
        Processes 2D data for all but LES/VER models

        Args:
            model: string, which model is being processed
                must be format in the directory system
            domain: string, which domain is being processed
            temperature: string, which SST is being processed
            variable: string, which variable is being processed
            mfiles: boolean, False for all variables and times are in one file
            mtype: string, denotes global or cartesian plane
            cmt: (optional, True) boolean,

        Returns:
            v: 3D array [time,x,y], the variable processed
            x: 1D array [x], zonal data (meters or degrees)
            y: 1D array [x], meridional data (meters or degrees)
            t: 1D array [t], time data (days)
    """
    x = 'lon'
    y = 'lat'

    rcemip = '/huracan/tank2/columbia/RCEMIP/'
    mpath  = rcemip+model+'/'+'RCE_'+domain+temperature+'/2D/'
    f = mpath+model+'_RCE_'+domain+temperature+'_2D_'+variable+'_'+str(cmt).zfill(3)+'-'+str(cmt+9).zfill(3)+'d.nc'

    ds = xr.open_dataset(f, decode_times=False)

    v = ds[variable].values
    x = ds[x].values
    y = ds[y].values

    labx = 0
    laby = 0
    locx = 0
    locy = 0

    ttt = 'time'
    t = ds[ttt].values
    t += (1/48)

    ds.close()
    return(v,x,y,t)

def process_SAM02D(model, domain, temperature, variable, mfiles,mtype,sam0):
    """
        Processes 2D data for all but LES/VER models

        Args:
            model: string, which model is being processed
                must be format in the directory system
            domain: string, which domain is being processed
            temperature: string, which SST is being processed
            variable: string, which variable is being processed
            mfiles: boolean, False for all variables and times are in one file
            mtype: string, denotes global or cartesian plane
            sam0: (optional, True) boolean,

        Returns:
            v: 3D array [time,x,y], the variable processed
            x: 1D array [x], zonal data (meters or degrees)
            y: 1D array [x], meridional data (meters or degrees)
            t: 1D array [t], time data (days)
    """

    x = 'lon'
    y = 'lat'
    rcemip = '/huracan/tank2/columbia/RCEMIP/'
    mpath  = rcemip+model+'/'+'RCE_'+domain+temperature+'/2D/'

    f = mpath+model+'_RCE_'+domain+temperature+'_2D_'+variable+'_000'+sam0+'.nc'

    ds = xr.open_dataset(f, decode_times=False)

    v = ds[variable].values
    x = ds[x].values
    y = ds[y].values

    ttt = 'time'
    t = ds[ttt].values

    ds.close()
    return(v,x,y,t)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MODEL PROPERTIES ---------------------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def file_properties(domain):

    
    a = plt.cm.tab20(np.linspace(0,1,20))
    b = plt.cm.Dark2(np.linspace(0,1,8))
    c = plt.cm.tab10(np.linspace(0,1,10))
    d = plt.cm.Set3(np.linspace(0,1,12))
    e = plt.cm.tab20b(np.linspace(0,1,20))
    f = plt.cm.tab20c(np.linspace(0,1,20))
    g = plt.cm.Set2(np.linspace(0,1,8))
    h = plt.cm.Set1(np.linspace(0,1,9))
    q = plt.cm.bone(np.linspace(0,1,9))

    if domain == 'large':
        # LARGE DOMAIN

        directory = ['CAM5_GCM','CAM6_GCM','CM1','CNRM-CM6-1','dam','ECHAM6_GCM','FV3',
                     'GEOS_GCM','ICON_GCM','ICON_LEM_CRM','ICON_NWP_CRM','IPSL-CM6',
                     'MESONH','MPAS','NICAM','SAM0-UNICON','SAM6.11.2','SAM_GCRM','SCALE',
                     'SP-CAM','SPX-CAM','UCLA-CRM','UKMO-GA7.1','UKMOi-vn11.0-CASIM',
                     'UKMOi-vn11.0-RA1-T','UKMOi-vn11.0-RA1-T-nocloud','WRF_COL_CRM',
                     'WRF-CRM','WRF_GCM_cps0','WRF_GCM_cps1','WRF_GCM_cps2',
                     'WRF_GCM_cps3','WRF_GCM_cps4','WRF_GCM_cps6']
        multi1d   = [True,True,False,True,True,False,True,True,False,False,False,True,
                     True,False,True,True,True,True,True,True,True,False,True,False,False,
                     False,False,False,False,False,False,False,False,False]
        multi2d   = [True,True,True,True,True,False,True,True,False,False,False,True,
                     True,True,True,True,True,True,True,True,True,True,True,False,False,
                     False,False,False,False,False,False,False,False,False]
        label     = ['CAM5-GCM','CAM6-GCM','CM1','CNRM-CM6','DAM','ECHAM6-GCM','FV3',
                     'GEOS-GCM','ICON-GCM','ICON-LEM-CRM','ICON-NWP-CRM','IPSL-CM6',
                     'MESONH','MPAS','NICAM','SAM0-UNICON','SAM-CRM','SAM-GCRM','SCALE',
                     'SP-CAM','SPX-CAM','UCLA-CRM','UKMO-GA7.1','UKMO-CASIM','UKMO-RA1-T',
                     'UKMO-RA1-T-nocloud','WRF-COL-CRM','WRF-CRM','WRF-GCM-cps0',
                     'WRF-GCM-cps1','WRF-GCM-cps2','WRF-GCM-cps3','WRF-GCM-cps4',
                     'WRF-GCM-cps6']
        gemoetry  = ['GCM','GCM','CRM','GCM','CRM','GCM','CRM','GCM','GCM','CRM','CRM',
                     'GCM','CRM','GCM','GCM','GCM','CRM','GCM','CRM','GCM','GCM','CRM',
                     'GCM','CRM','CRM','CRM','CRM','CRM','GCM','GCM','GCM','GCM','GCM',
                     'GCM']
        height    = ['zg_avg','zg_avg','z','zg_avg','z','zg_avg','zg_avg','zg',
                     'height_avg','height_avg','height_avg','zg_avg','altitude','height',
                     'z','zg_avg','z','z','lev','z_avg','z_avg','zt','rho_height_levels',
                     'rholevdm_zsea_rho','rholevdm_zsea_rho','rholevdm_zsea_rho','zg_avg',
                     'zg_avg','h_avg','h_avg','h_avg','h_avg','h_avg','h_avg']
        color     = [e[6],e[7],f[0],b[3],g[0],c[3],c[8],d[3],c[5],e[9],e[8],
                     np.array([0.,0.,0.,1.]),f[4],d[4],h[5],e[5],e[13],e[12],b[0],a[18],
                     a[19],d[11],e[16],e[17],e[18],c[6],e[0],e[1],e[2],e[3],f[12],f[13],
                     f[14],f[15]]

        model_properties = pd.DataFrame({'DIRECTORY':directory,
                                         'LABEL':label,
                                         'GEOMETRY':gemoetry,
                                         'HEIGHT':height,
                                         'COLOR':color,
                                         'MULTI_1D':multi1d,
                                         'MULTI_2D':multi2d})

    if domain == 'small':
        # SMALL DOMAIN

        directory = ['CAM5_GCM','CAM6_GCM','CM1','CM1','CM1','CNRM-CM6-1','DALES','DALES',
                     'DALES','DALES-damping','DALES-damping','DALES_damping_rad','dam','GEOS_GCM',
                     'ICON_LEM_CRM','ICON_LEM_CRM','ICON_LEM_CRM','ICON_NWP_CRM','MESONH',
                     'MESONH','MESONH','MicroHH','MicroHH','MicroHH','MPAS','SAM6.11.2',
                     'SAM_CRM','SAM_CRM','SCALE','UCLA-CRM','UKMO-GA7.1',
                     'UKMOi-vn11.0-CASIM','UKMOi-vn11.0-RA1-T-hrad','UKMOi-vn11.0-RA1-T',
                     'UKMOi-vn11.0-RA1-T-nocloud','WRF_COL_CRM','WRF-CRM','WRF_GCM_cps0',
                     'WRF_GCM_cps1','WRF_GCM_cps2','WRF_GCM_cps3','WRF_GCM_cps4',
                     'WRF_GCM_cps6']
        multi1d   = [True,True,False,False,False,True,True,True,True,True,True,True,True,True,
                     False,False,False,False,True,True,True,False,False,False,False,True,
                     True,True,True,False,True,False,False,False,False,False,False,False,
                     False,False,False,False,False]
        multi2d   = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,
                     False,False,False,False,True,True,True,True,True,True,False,True,
                     True,True,True,True,True,False,False,False,False,False,False,False,
                     False,False,False,False,False]
        label     = ['CAM5-GCM','CAM6-GCM','CM1','CM1-VER','CM1-LES','CNRM-CM6','DALES',
                     'DALES-VER','DALES-LES','DALES-damping','DALES-damping-VER','DALES-damping-rad-VER','DAM',
                     'GEOS-GCM','ICON-LEM-CRM','ICON-LEM-VER','ICON-LEM-LES',
                     'ICON-NWP-CRM','MESONH','MESONH-VER','MESONH-LES','MicroHH',
                     'MicroHH-VER','MicroHH-LES','MPAS','SAM-CRM','SAM-CRM-VER',
                     'SAM-CRM-LES','SCALE','UCLA-CRM','UKMO-GA7.1','UKMO-CASIM',
                     'UKMO-RA1-T-hrad','UKMO-RA1-T','UKMO-RA1-T-nocloud','WRF-COL-CRM',
                     'WRF-CRM','WRF-GCM-cps0','WRF-GCM-cps1','WRF-GCM-cps2',
                     'WRF-GCM-cps3','WRF-GCM-cps4','WRF-GCM-cps6']
        gemoetry   = ['GCM','GCM','CRM','vert','les','GCM','CRM','vert','les','CRM',
                      'vert','vert','CRM','GCM','CRM','vert','les','CRM','CRM','vert','les',
                      'CRM','vert','les','GCM','CRM','vert','les','CRM','CRM','GCM','CRM',
                      'CRM','CRM','CRM','CRM','CRM','GCM','GCM','GCM','GCM','GCM','GCM']
        height     = ['zg_avg','zg_avg','z','z','z','zg_avg','zt','zt','zt','zt','zt','zt','z',
                      'zg_avg','height_avg','height_avg','height_avg','height_avg',
                      'altitude','altitude','altitude','z','z','z','height','z','z','z',
                      'lev','zt','rho_height_levels','rholevdm_zsea_rho',
                      'rholevdm_zsea_rho','rholevdm_zsea_rho','rholevdm_zsea_rho',
                      'zg_avg','Height','h_avg','h_avg','h_avg','h_avg','h_avg','h_avg']
        color      = [e[6],e[7],f[0],f[1],f[2],b[3],b[7],q[3],q[4],q[5],q[6],q[7],g[0],d[3],
                      e[9],e[10],e[11],e[8],f[4],f[5],f[6],h[3],a[8],a[9],d[4],e[13],
                      e[14],e[15],b[0],d[11],e[16],e[17],e[18],e[19],c[6],e[0],e[1],e[2],
                      e[3],f[12],f[13],f[14],f[15]]

        model_properties = pd.DataFrame({'DIRECTORY':directory,
                                         'LABEL':label,
                                         'GEOMETRY':gemoetry,
                                         'HEIGHT':height,
                                         'COLOR':color,
                                         'MULTI_1D':multi1d,
                                         'MULTI_2D':multi2d})

    if domain == 'diff':
        # DIFF DOMAIN

        directory = ['CAM5_GCM','CAM6_GCM','CM1','CNRM-CM6-1','dam','GEOS_GCM',
                     'ICON_LEM_CRM','ICON_NWP_CRM','MESONH','MPAS','SAM6.11.2','SCALE',
                     'UCLA-CRM','UKMO-GA7.1','UKMOi-vn11.0-CASIM','UKMOi-vn11.0-RA1-T',
                     'UKMOi-vn11.0-RA1-T-nocloud','WRF_COL_CRM','WRF-CRM','WRF_GCM_cps0',
                     'WRF_GCM_cps1','WRF_GCM_cps2','WRF_GCM_cps3','WRF_GCM_cps4',
                     'WRF_GCM_cps6']
        multi1d   = [True,True,False,True,True,True,False,False,True,False,True,True,
                     False,True,False,False,False,False,False,False,False,False,False,
                     False,False]
        multi2d   = [True,True,True,True,True,True,False,False,True,False,True,True,True,
                     True,False,False,False,False,False,False,False,False,False,False,
                     False]
        label     = ['CAM5-GCM','CAM6-GCM','CM1','CNRM-CM6','DAM','GEOS-GCM',
                     'ICON-LEM-CRM','ICON-NWP-CRM','MESONH','MPAS','SAM-CRM','SCALE',
                     'UCLA-CRM','UKMO-GA7.1','UKMO-CASIM','UKMO-\nRA1-T(L)-hrad(S)',
                     'UKMO-\nRA1-T-nocloud','WRF-COL-CRM','WRF-CRM','WRF-GCM-cps0',
                     'WRF-GCM-cps1','WRF-GCM-cps2','WRF-GCM-cps3','WRF-GCM-cps4',
                     'WRF-GCM-cps6']
        geometry  = ['GCM','GCM','CRM','GCM','CRM','GCM','CRM','CRM','CRM','GCM','CRM',
                     'CRM','CRM','GCM','CRM','CRM','CRM','CRM','CRM','GCM','GCM','GCM',
                     'GCM','GCM','GCM']

        height    = ['zg_avg','zg_avg','z','zg_avg','z','zg_avg','height_avg',
                     'height_avg','altitude','height','z','lev','zt','rho_height_levels',
                     'rholevdm_zsea_rho','rholevdm_zsea_rho','rholevdm_zsea_rho','zg_avg',
                     'Height','h_avg','h_avg','h_avg','h_avg','h_avg','h_avg']

        color     = [e[6],e[7],f[0],b[3],g[0],d[3],e[9],e[8],f[4],d[4],e[13],b[0],d[11],
                     e[16],e[17],e[18],c[6],e[0],e[1],e[2],e[3],f[12],f[13],f[14],f[15]]

        model_properties = pd.DataFrame({'DIRECTORY':directory,
                                         'LABEL':label,
                                         'GEOMETRY':geometry,
                                         'HEIGHT':height,
                                         'COLOR':color,
                                         'MULTI_1D':multi1d,
                                         'MULTI_2D':multi2d})

    return(model_properties)

def conv_scheme():
    exp_models = ['CM1','DALES','DALES-damping','DAM','FV3','ICON-LEM-CRM','ICON-NWP-CRM',
                  'MESONH','MicroHH','MPAS','NICAM','SAM-CRM','SAM-GCRM','SCALE','UCLA-CRM',
                  'UKMO-CASIM','UKMO-RA1-T-hrad','UKMO-RA1-T','UKMO-RA1-T-nocloud','WRF-COL-CRM',
                  'WRF-CRM','CM1-VER','CM1-LES','DALES-VER','DALES-LES','DALES-damping-VER',
                  'ICON-LEM-LES','ICON-LEM-VER','MESONH-VER','MESONH-LES','MicroHH-VER',
                  'MicroHH-LES','SAM-CRM-VER','SAM-CRM-LES']
    par_models = ['CAM5-GCM','CAM6-GCM','CNRM-CM6','ECHAM6-GCM','GEOS-GCM','ICON-GCM','IPSL-CM6',
                  'SAM0-UNICON','SP-CAM','SPX-CAM','UKMO-GA7.1','WRF-GCM-cps0','WRF-GCM-cps1',
                  'WRF-GCM-cps2','WRF-GCM-cps3','WRF-GCM-cps4','WRF-GCM-cps6']
    return(exp_models, par_models)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# END FILE PROCESSING SCRIPT ------------------------------------------------ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
