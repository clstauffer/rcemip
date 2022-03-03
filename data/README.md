# Derived Data used in Stauffer and Wing (2022, in review)

## Files

### Cloud Anvil Height, Temperature, and Cloud Fraction

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

### Radiatively-Driven Divergence Profiles

File Name | Description
---|---
rad-driven-div_profiles.tar.gz | profiles of radiatively-driven divergence for all models, domains, and SSTs

Variable | Description | Unit
---|---|---
ss_avg | static stability | 
pa_avg | pressure | hPa
ta_avg | temperature | K
qr_avg | clear sky radiative cooling | day<sup>-1</sup>
wa_full | clear sky vertical velocity | 
rd_full | radiatively-driven divergence | day<sup>-1</sup>
wa_300s | wa_full using ss_avg at 300 K | 
rd_300s | rd_full using ss_avg at 300 K | day<sup>-1</sup>
wa_300q | wa_full using qr_avg at 300 K | 
rd_300q | rd_full using qr_avg at 300 K | day<sup>-1</sup>
zg_avg | height | km

### Peak Radiatively-Driven Divergence Properties

File Name | Description
---|---
rdiv_large.csv | large domain peak Rd properties
rdiv_small.csv | small domain peak Rd properties

Variable | Description | Unit
---|---|---
LABEL | Model Name | N/A
RDFULL295 | 295 K peak Rd | day<sup>-1</sup>
RDFULL300 | 300 K peak Rd | day<sup>-1</sup>
RDFULL305 | 305 K peak Rd | day<sup>-1</sup>
PAFULL295 | 295 K Pressure at peak Rd | hPa
PAFULL300 | 300 K Pressure at peak Rd | hPa
PAFULL305 | 305 K Pressure at peak Rd | hPa
ZGFULL295 | 295 K height at peak Rd | km
ZGFULL300 | 300 K height at peak Rd | km
ZGFULL305 | 305 K height at peak Rd | km
TAFULL295 | 295 K temperature at peak Rd | K
TAFULL300 | 300 K temperature at peak Rd | K
TAFULL305 | 305 K temperature at peak Rd | K
RD300S295 | 295 K peak Rd using S(300 K) | day<sup>-1</sup>
RD300S300 | 300 K peak Rd using S(300 K) | day<sup>-1</sup>
RD300S305 | 305 K peak Rd using S(300 K) | day<sup>-1</sup>
PA300S295 | 295 K Pressure at peak Rd using S(300 K) | hPa
PA300S300 | 300 K Pressure at peak Rd using S(300 K) | hPa
PA300S305 | 305 K Pressure at peak Rd using S(300 K) | hPa
ZG300S295 | 295 K height at peak Rd using S(300 K) | km
ZG300S300 | 300 K height at peak Rd using S(300 K) | km
ZG300S305 | 305 K height at peak Rd using S(300 K) | km
TA300S295 | 295 K temperature at peak Rd using S(300 K) | K
TA300S300 | 300 K temperature at peak Rd using S(300 K) | K
TA300S305 | 305 K temperature at peak Rd using S(300 K) | K
RD300Q295 | 295 K peak Rd using Qr(300 K) | day<sup>-1</sup>
RD300Q300 | 300 K peak Rd using Qr(300 K) | day<sup>-1</sup>
RD300Q305 | 305 K peak Rd using Qr(300 K) | day<sup>-1</sup>
PA300Q295 | 295 K Pressure at peak Rd using Qr(300 K) | hPa
PA300Q300 | 300 K Pressure at peak Rd using Qr(300 K) | hPa
PA300Q305 | 305 K Pressure at peak Rd using Qr(300 K) | hPa
ZG300Q295 | 295 K height at peak Rd using Qr(300 K) | km
ZG300Q300 | 300 K height at peak Rd using Qr(300 K) | km
ZG300Q305 | 305 K height at peak Rd using Qr(300 K) | km
TA300Q295 | 295 K temperature at peak Rd using Qr(300 K) | K
TA300Q300 | 300 K temperature at peak Rd using Qr(300 K) | K
TA300Q305 | 305 K temperature at peak Rd using Qr(300 K) | K
STAB295 | 295 K static stability at peak Rd |
STAB300 | 300 K static stability at peak Rd |
STAB305 | 305 K static stability at peak Rd |
S220295 | 295 K 220K static stability at peak Rd |
S220300 | 300 K 220K static stability at peak Rd |
S220305 | 305 K 220K static stability at peak Rd |
Cr | RCEMIP Red Color | N/A
Cb | RCEMIP Blue Color | N/A
Cg | RCEMIP Green Color | N/A
Ca | RCEMIP Alpha Color | N/A

### Conditional Statistics Profiles (used for mid-level scaling diagnostic)

File Name | Description
---|---
midlevel_profiles_1D-derived.tar.gz | conditional statistics using `cfv1` for all models, domains, and SSTs
midlevel_profiles_3D-derived.tar.gz | conditional statistics using `cfv2` for all models, domains, and SSTs

The derived profiles are below, for a complete list of conditional statistics profiles included in this data set please see `conditional_statistics.md`

Variable | Description | Unit
---|---|---
z | height | km
tabs_mean | temperature | K
cld_mean | cloud fraction | -
rhenv_mean | environmental relative humidity | -
JT_mean | 
Jp_int | troposphere-integrated radiative cooling rate | 
cld_scaling | cloud fraction diagnosed by MLS | -

### Mid-level propertye metrics as used in Stauffer and Wing (2022, in review)

Variable description is defiined in Section 2.4.1 of Stauffer and Wing (2022, in review)

File Name | Description | Units
---|---|---
midlevel-cf_metrics_large_exp.csv | N/A
midlevel-cf_metrics_large_par.csv | N/A
mlsd_metrics_large_exp.csv | N/A
rhum_metrics_large_exp.csv | 
wavg_metrics_large_exp.csv | 
dsea_metrics_large_exp.csv | 
javg_metrics_large_exp.csv | 
jint_metrics_large_exp.csv | 

Below, $\gamma$ corresponds to the variable corresponding to whichever file in the table above

Variable | Description
---|---
Model | Model Name
Zavg | $<\gamma_{avg}>_z$
Zrng | $<\gamma_{range}>_z$
Zdif | $<\gamma_{\Delta}>_z$
Tavg | $<\gamma_{avg}>_T$
Trng | $<\gamma_{range}>_T$
Tdif | $<\gamma_{\Delta}>_T$
Color | RCEMIP colors; [red,blue,green,alpha]
