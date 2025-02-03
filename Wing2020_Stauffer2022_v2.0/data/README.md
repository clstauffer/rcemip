# Derived data used in Stauffer and Wing (2022)

## Files

### Cloud Anvil Height, Temperature, and Cloud Fraction

The script used to calculate ``cfv1`` and ``cfv2`` is provided at ``stauffer-wing_2022/scripts/cloudfraction.py``

File Name | Domain | Cloud Fraction Definition
---|---|---
anvil-properties_large_cfv1.csv | large | cfv1
anvil-properties_large_cfv2.csv | large | cfv2
anvil-properties_small_cfv1.csv | small | cfv1
anvil-properties_small_cfv2.csv | small | cfv2

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

The script used to calculate the below profiles is provided at ``stauffer-wing_2022/scripts/divergence.py``

File Name | Description
---|---
rad-driven-div_profiles.tar.gz | profiles of radiatively-driven divergence for all models, domains, and SSTs

Variable | Description | Unit
---|---|---
ss_avg | static stability | K Pa<sup>-1</sup>
pa_avg | pressure | Pa
ta_avg | temperature | K
qr_avg | clear sky radiative cooling | day<sup>-1</sup>
wa_full | clear sky vertical velocity | Pa s<sup>-1</sup>
rd_full | radiatively-driven divergence | day<sup>-1</sup>
wa_300s | wa_full using ss_avg at 300 K | Pa s<sup>-1</sup>
rd_300s | rd_full using ss_avg at 300 K | day<sup>-1</sup>
wa_300q | wa_full using qr_avg at 300 K | Pa s<sup>-1</sup>
rd_300q | rd_full using qr_avg at 300 K | day<sup>-1</sup>
zg_avg | height | m

### Peak Radiatively-Driven Divergence Properties

File Name | Description
---|---
rdiv-properties_large.csv | large domain peak Rd properties
rdiv-properties_small.csv | small domain peak Rd properties

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
STAB295 | 295 K static stability at peak Rd | K Pa<sup>-1</sup>
STAB300 | 300 K static stability at peak Rd | K Pa<sup>-1</sup>
STAB305 | 305 K static stability at peak Rd | K Pa<sup>-1</sup>
S220295 | 295 K 220K static stability at peak Rd | K Pa<sup>-1</sup>
S220300 | 300 K 220K static stability at peak Rd | K Pa<sup>-1</sup>
S220305 | 305 K 220K static stability at peak Rd | K Pa<sup>-1</sup>
Cr | RCEMIP Red Color | N/A
Cb | RCEMIP Blue Color | N/A
Cg | RCEMIP Green Color | N/A
Ca | RCEMIP Alpha Color | N/A

### Conditional Statistics Profiles (used for mid-level scaling diagnostic)

The script used to calculate the conditional statistics profiles is provided at ``stauffer-wing_2022/scripts/conditionalstats.py``. These follow the definitions used in SAM6.11.2, conditions used can be found in the above mentioned script.

File Name | Description
---|---
midlevel_profiles_cfv1.tar.gz | conditional statistics using `cfv1` for all models, domains, and SSTs
midlevel_profiles_cfv2.tar.gz | conditional statistics using `cfv2` for all models, domains, and SSTs

The derived profiles are below, for a complete list of conditional statistics profiles included in this data set please see `conditional_statistics.md`

Variable | Description | Unit
---|---|---
z | height | m
tabs_mean | temperature | K
cld_mean | cloud fraction | -
rhenv_mean | environmental relative humidity | -
Jp_int | troposphere-integrated radiative cooling rate | W m<sup>-1</sup>
cld_scaling | cloud fraction diagnosed by MLS | -

### Mid-level property metrics as used in Stauffer and Wing (2022)

The script used to calculate the mid-level metrics is provided at ``stauffer-wing_2022/scripts/midlevelscaling.py``

Variable description is defiined in Section 2.4.1 of Stauffer and Wing (2022)

File Name | Description | Units
---|---|---
mlcf_metrics_large_exp.csv | mid-level cloud fraction, explicit convection | -
mlcf_metrics_large_par.csv | mid-level cloud fraction, parameterized convection | -
mlsd_metrics_large_exp.csv | mid-level scaling diagnostic, explicit convection | -
rhum_metrics_large_exp.csv | enviornmental relative humidity | -
wavg_metrics_large_exp.csv | cloudy updraft | m s<sup>-1</sup>
dsea_metrics_large_exp.csv | DSE excess | J m<sup>-3</sup>
javg_metrics_large_exp.csv | radiative cooling rate | W m<sup>-2</sup> K<sup>-1</sup>
jint_metrics_large_exp.csv | integrated radiative cooling rate | W m<sup>-2</sup>

Below, &gamma; corresponds to the variable corresponding to whichever file in the table above

Variable | Description
---|---
Model | Model Name
Zavg | &gamma;<sub>avg<sub>z</sub></sub>
Zrng | &gamma;<sub>rng<sub>z</sub></sub>
Zdif | &gamma;<sub>&Delta;<sub>z</sub></sub>
Tavg | &gamma;<sub>avg<sub>T</sub></sub>
Trng | &gamma;<sub>rng<sub>T</sub></sub>
Tdif | &gamma;<sub>&Delta;<sub>T</sub></sub>
Color | RCEMIP colors; [red,blue,green,alpha]
