# Data and Scripts used in Stauffer and Wing (2022) (SW22)

## PROFILES
  * ./ENV/cf1D/ : contains temporal- and domain-averaged profiles using the 
              1D model output provided by the contributors and contains 
              the following variables
    * zg_avg: height coordinate [m]
    * cfv0_avg: cloud fraction
    * hur_avg: relative humidity [%]
    * hus_avg: specific humidity [%]
    * ta_avg: temperature [K]
    * pa_avg: pressure [Pa]
    * tw_avg: total cloud water
    * Cr: red color for a model
    * Cg: green color for a model
    * Cb: blue color for a model
    * Ca: transparency for a model
  * ./ENV/cf3D/ : contains temporal- and domain-averaged profiles using the 
              3D model output provided by the contributors, and contains 
              the following variables
    * zg_avg: height coordinate [m]
    * cfv1_avg: cloud fraction (see SW22 for the calculation)
    * cfv2_avg: cloud fraction (see SW22 for the calculation)
    * hur_avg: relative humidity [%]
    * hus_avg: specific humidity [%]
    * ta_avg: temperature [K]
    * pa_avg: pressure [Pa]
    * tw_avg: total cloud water
    * Cr: red color for a model
    * Cg: green color for a model
    * Cb: blue color for a model
    * Ca: transparency for a model
  * ./MLS/cfv2/ : contains temporal- and domain-averaged profiles of the
                  various variables used in the mid-level cloud diagnostic
                  used in SW22, see ``midlevelscaling.py`` for more info. 
                  Essential variables from the file are the following
    * Jp_int: tropospheric radiative cooling rate
    * wcld_mean: cloud updraft
    * tabs_mean: temperature
    * rhenv_mean: environmental relative humidity
    * dscor_mean: dry static energy excess carried upward by clouds
    * cld_scaling: cloud fraction as predicted by the mid-level scaling diagnostic
  * ./RDIV/ : contains temporal- and domain-averaged profiles of the
              components of the radiatively-driven divergence used in SW22
    * ss_avg: static stability [KPa-]
    * pa_avg: pressure [Pa]
    * ta_avg: temperature [K]
    * qr_avg: clear-sky radiative cooling rate [Ks-1]
    * wa_full: clear-sky radiatively-driven vertical motion [Pas-]
    * rd_full: radiatively-driven divergence [day-]
    * wa_300s: clear-sky radiatively-driven vertical motion [Pas-]
               using 300 K static stability
    * rd_300s: radiatively-driven divergence [day-]
               using 300 K static stability
    * wa_300q: clear-sky radiatively-driven vertical motion [Pas-]
               using 300 K clear-sky radiative cooling rate
    * rd_300q: radiatively-driven divergence [day-]
               using 300 K clear-sky radiative cooling rate
    * zg_avg: height [m]
  * ./CONDSTATS/cfv2/ : contains domain-averaged profiles of various
                        conditional statistics used in the scaling 
                        diagnostic for mid-level cloud fraction using 
                        see midlevelscaling.py and conditionalstats.py 
                        for more information on the contents

## TABLES
  * Mid-level metrics (used in Figure 11 of SW22)
    * ``var``_metrics_large_exp.csv : 
      * dsea: 
      * javg: 
      * jint: 
      * mlsd: 
      * rhum: 
      * wavg: 
    * midlevel-cf_metrics_large_``conv``.csv: 
      * conv: exp or par - explicit or parameterized convection
  * Radiatively-driven divergence (used in Figures 8,9,10 of SW22)
    * rdiv_large.csv : 
    * rdiv_small.csv : 
  * Cloud fraction of the format: ``domain``_``cfv``_all.csv
    * domain: small or large
    * cfv: cfv0, cfv1, cfv2 - definition of cloud fraction, see SW22

## SCRIPTS
  * cloudfraction.py : 
  * conditionalstats.py : 
  * divergence.py : 
  * midlevelscaling.py : 
