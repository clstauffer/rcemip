#%%###################################################################
### IMPORT LIBRARIES #################################################
######################################################################
from helpers import *
"""
Fig 12  - 300 K
Fig S19 - 295 K
Fig S20 - 305 K
Fig 16  - d(295,305)

Fig S21 - d(295,300) vs d(300,305)

Fig S23 - d(295,305) w/ 0-point conn
Fig S22 - 300 K w/ 0-point conn

Fig S24 - d(295,305) w/ scaled PW
Fig S24 - 300 K w/ scaled PW

itype - conn4,conn1
ctype - crh,pw
ptype - show,save
"""

#%%###################################################################
### PROCESS DATA
######################################################################
domain,itype,vtype,ptype = 'large','conn4','crh','save' # str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4])

df = pd.read_csv('./data/metrics_large_v2.0.csv',sep='\t')
df295,df300,df305 = get_data(df,'295'),get_data(df,'300'),get_data(df,'305')

#%%###################################################################
### Figure 12/S19/S20/S22/S24 ########################################
######################################################################
sf295 = df295.sort_values(by=['scheme','SUBFRAC'],ascending=True,na_position='first')
sf300 = df300.sort_values(by=['scheme','SUBFRAC'],ascending=True,na_position='first')
sf305 = df305.sort_values(by=['scheme','SUBFRAC'],ascending=True,na_position='first')

if vtype == 'pw':
    ylabelss = ['$f_{sub}$','$I_{ORG}$','$\sigma^2_{PW/<PW>}$']
    ylimss = [[0,1.0],[0,1.0],[0,0.60]]
if vtype == 'crh':
    ylabelss = ['$f_{sub}$','$I_{ORG}$','$\sigma^2_{CRH}$']
    ylimss = [[0,1.0],[0,1.0],[0,0.10]]

plot_metric_scatter(sf295,vtype,ylimss,ylabelss,False,'Large Domain 295 K Metrics','wing2020_figS19_metrics_'+domain+'295_'+itype+'_'+vtype+'_'+ptype+'.pdf',ptype)
plot_metric_scatter(sf300,vtype,ylimss,ylabelss,False,'Large Domain 300 K Metrics','wing2020_fig12_metrics_'+domain+'300_'+itype+'_'+vtype+'_'+ptype+'.pdf',ptype)
plot_metric_scatter(sf305,vtype,ylimss,ylabelss,False,'Large Domain 305 K Metrics','wing2020_figS20_metrics_'+domain+'305_'+itype+'_'+vtype+'_'+ptype+'.pdf',ptype)

#%%###################################################################
### Figure 16/S23/S25 ################################################
######################################################################
subf_slopes = calc_roc(df295,df300,df305,df295.MODEL.values,'SUBFRAC','large')
iorg_slopes = calc_roc(df295,df300,df305,df295.MODEL.values,'IORG','large')
vcrh_slopes = calc_roc(df295,df300,df305,df295.MODEL.values,'VCRH','large')

subf_slopes = subf_slopes.sort_values(by=['scheme','295-305'],ascending=True,na_position='first')
iorg_slopes = iorg_slopes.reindex(subf_slopes.index)
vcrh_slopes = vcrh_slopes.reindex(subf_slopes.index)
slopes295305 = pd.DataFrame({'MODEL':subf_slopes.MODEL.values,'SUBFRAC':subf_slopes['295-305'],'IORG':iorg_slopes['295-305'],'VCRH':vcrh_slopes['295-305']})

if vtype == 'pw':
    ylabelss = ['d$f_{sub}$\dSST','d$I_{ORG}$\dSST','d$\sigma^2_{PW/<PW>}$\dSST']
    ylimss = [[-0.04,0.04],[-0.04,0.04],[-0.025,0.025]]
if vtype == 'crh':
    ylabelss = ['d$f_{sub}$\dSST','d$I_{ORG}$\dSST','d$\sigma^2_{CRH}$\dSST']
    ylimss = [[-0.04,0.04],[-0.04,0.04],[-0.006,0.006]]

plot_metric_scatter(slopes295305,vtype,ylimss,ylabelss,True,'Rate of Change of Aggregation Metrics in RCE_'+domain,'wing2020_fig16_metrics_'+domain+'295305_'+itype+'_'+vtype+'_'+ptype+'.pdf',ptype)

#%%###################################################################
### Figure S21 #######################################################
######################################################################
subf_slopes = calc_roc(df295,df300,df305,df.MODEL.values,'SUBFRAC','large')
iorg_slopes = calc_roc(df295,df300,df305,df.MODEL.values,'IORG','large')
vcrh_slopes = calc_roc(df295,df300,df305,df.MODEL.values,'VCRH','large')

# subf_slopes = subf_slopes.sort_values(by=['scheme','295-305'],ascending=True,na_position='first')
subf_slopes = subf_slopes.sort_values(by=['scheme','MODEL'],ascending=True,na_position='first')
iorg_slopes = iorg_slopes.reindex(subf_slopes.index)
vcrh_slopes = vcrh_slopes.reindex(subf_slopes.index)

plot_roc_comp(subf_slopes,iorg_slopes,vcrh_slopes,vtype,'wing2020_figS21_metrics_'+domain+'_295300_300305_'+itype+'_'+vtype+'_'+ptype+'.pdf',ptype)

#%%###################################################################
### END ##############################################################
######################################################################