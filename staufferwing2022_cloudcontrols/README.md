# Derived Data used in Stauffer and Wing (2022)

## Files

### Cloud Anvil Height, Temperature, and Cloud Fraction

#### File list
File Name | Domain | Cloud Fraction Definition | Model Convection Type
---|---|---|---
small_cfv1_all.csv | small | cfv1 | explicit and parameterized
small_cfv1_exp.csv | small | cfv1 | explicit
small_cfv1_par.csv | small | cfv1 | parameterized
large_cfv1_all.csv | large | cfv1 | explicit and parameterized
large_cfv1_exp.csv | large | cfv1 | explicit
large_cfv1_par.csv | large | cfv1 | parameterized
small_cfv2_all.csv | small | cfv2 | explicit and parameterized
small_cfv2_exp.csv | small | cfv2 | explicit
small_cfv2_par.csv | small | cfv2 | parameterized
large_cfv2_all.csv | large | cfv2 | explicit and parameterized
large_cfv2_exp.csv | large | cfv2 | explicit
large_cfv2_par.csv | large | cfv2 | parameterized

#### Variable List
Variable | Description | Unit
---|---|---
LABEL | Model Name | N/A
CF295 | Anvil Cloud Fraction for 295 K | -
CF300 | Anvil Cloud Fraction for 300 K | -
CF305 | Anvil Cloud Fraction for 305 K | -
AT295 | Anvil Temperature for 295 K | K
AT300 | Anvil Temperature for 300 K | K
AT305 | Anvil Temperature for 305 K | K
AZ295 | Anvil Height for 295 K | km
AZ300 | Anvil Height for 300 K | km
AZ305 | Anvil Height for 305 K | km
Cr | RCEMIP Red Color | N/A
Cb | RCEMIP Blue Color | N/A
Cg | RCEMIP Green Color | N/A
Ca | RCEMIP Alpha Color | N/A

rad-driven-div_profiles.tar.gz
rdiv_large.csv
rdiv_small.csv

midlevel-cf_metrics_large_exp.csv
midlevel-cf_metrics_large_par.csv
midlevel_profiles_1D-derived.tar.gz
midlevel_profiles_3D-derived.tar.gz
mlsd_metrics_large_exp.csv
rhum_metrics_large_exp.csv
wavg_metrics_large_exp.csv
dsea_metrics_large_exp.csv
javg_metrics_large_exp.csv
jint_metrics_large_exp.csv

## PROFILES
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
