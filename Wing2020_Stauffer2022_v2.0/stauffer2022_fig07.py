import numpy as np
import pandas as pd
import proplot as pplt
import processData

#%%
def divvals(vals): # normalize data around 300 K value
    vals_norm = pd.DataFrame({'295K':vals['295K'].div(vals['300K']),
                              '300K':vals['300K'].div(vals['300K']),
                              '305K':vals['305K'].div(vals['300K'])})
    return(vals_norm)

def processmodels(fl,thr): # make the cloudfraction dataframes
    var = pd.read_csv(fl)#,sep='\t')
    for i in range(len(var)): # filter out models w/o share data
        if var.LABEL[i] not in thr:
            var.iloc[i] = np.nan
    var=var.dropna()
    var=var.sort_values('LABEL')
    var=var.reset_index()

    var_val = var[['CF295','CF300','CF305']]
    var_tmp = var[['AT295','AT300','AT305']]
    var_hgt = var[['AZ295','AZ300','AZ305']]
    var_val = var_val.rename(columns={'CF295':'295K','CF300':'300K','CF305':'305K'})
    var_tmp = var_tmp.rename(columns={'AT295':'295K','AT300':'300K','AT305':'305K'})
    var_hgt = var_hgt.rename(columns={'AZ295':'295K','AZ300':'300K','AZ305':'305K'})

    var_val_norm = divvals(var_val)
    var_tmp_norm = divvals(var_tmp)
    var_hgt_norm = divvals(var_hgt)

    return(var,var_val,var_tmp,var_hgt,var_val_norm,var_tmp_norm,var_hgt_norm)

#%%
domain,cfversion='large','cfv2'
if domain == 'large':
    three = ['CAM5-GCM','CAM6-GCM','CM1','CNRM-CM6',
            'GEOS-GCM','ICON-LEM-CRM','MESONH',
            'MPAS','NICAM','SAM0-UNICON','SAM-CRM',
            'SAM-GCRM','SCALE','SP-CAM','SPX-CAM',
            'UKMO-GA7.1','UKMO-CASIM','UKMO-RA1-T',
            'UKMO-RA1-T-nocloud']
if domain == 'small':
    three = ['CM1','CM1-VER','DAM','ICON-LEM-CRM',
             'ICON-LEM-LES','ICON-LEM-VER','MESONH',
             'MESONH-VER','SAM-CRM','SCALE','UKMO-CASIM',
             'UKMO-RA1-T-hrad','UKMO-RA1-T-nocloud','UKMO-RA1-T']
three = sorted(three)

models = processData.file_properties(domain)

psave = 'save'

#%%
#%% CLOUD FRACTION
cf,cf_val,cf_tmp,cf_hgt,___,___,___ = processmodels('./data/anvil-properties_'+domain+'_'+cfversion+'.csv',three)

#%% DIVERGENCE
fdiv = './data/rdiv-properties_'+domain+'.csv'
div = pd.read_csv(fdiv)#,sep='\t')

for i in range(len(div)):
    if div.LABEL[i] not in three:
        div.iloc[i] = np.nan
div=div.dropna()
div=div.sort_values('LABEL')
div=div.reset_index()

rf=['RDFULL295','RDFULL300','RDFULL305']
tf=['TAFULL295','TAFULL300','TAFULL305']
zf=['ZGFULL295','ZGFULL300','ZGFULL305']
rdf_val_full,rdf_tmp_full,rdf_hgt_full = div[rf],div[tf],div[zf]
rdf_val_full = rdf_val_full.rename(columns={rf[0]:'295K',rf[1]:'300K',rf[2]:'305K'})
rdf_tmp_full = rdf_tmp_full.rename(columns={tf[0]:'295K',tf[1]:'300K',tf[2]:'305K'})
rdf_hgt_full = rdf_hgt_full.rename(columns={zf[0]:'295K',zf[1]:'300K',zf[2]:'305K'})

#%%
## METRICS
mets = pd.read_csv('./data/metrics_large_v2.0.csv',sep='\t')
if domain == 'small':
    mets = mets.drop(columns=['S295','S300','S305'])
for i in range(len(mets.MODEL)):
    if mets.MODEL[i] not in three:
        mets.iloc[i] = np.nan
mets=mets.dropna()
mets=mets.sort_values('MODEL')
mets=mets.reset_index()

#%%
## MODEL ATTRIBUTES
# mmcol = []
# for i in range(len(three)):
#     mmcol.append([cf.Cr[i],cf.Cb[i],cf.Cg[i],cf.Ca[i]])
mlabcol = pd.DataFrame({'LABEL':div.LABEL})#,'COLOR':mmcol})
if domain == 'large':
    mtype = ['par','par','exp','par','par','exp',
             'exp','exp','exp','exp','exp','par','exp',
             'par','par','exp','par','exp','exp']
if domain == 'small':
    mtype = ['exp','exp','exp','exp','exp','exp',
             'exp','exp','exp','exp','exp','exp',
             'exp','exp']

#%%
## DIVERGENCE AND CLOUD FRACTION DECREASE WITH SST
rd_dec = rdf_val_full['305K']<rdf_val_full['295K']
cf_dec = cf_val['305K']<cf_val['295K']

data = {'Model':mlabcol.LABEL,'Scheme':mtype,'Rd Decreases':rd_dec,'CF Decreases':cf_dec}

decreases = pd.DataFrame(data)

#%%
## COLOR CODE BASED ON THEORY WORKING OR NOT
cbr,cbb,cbg = np.array([217/255,95/255,2/255,1]),np.array([117/255,112/255,179/255,1]),np.array([27/255,158/255,119/255,1])
fc,ec=[],[]
for i in range(len(decreases)):
    if decreases['Rd Decreases'][i] == True and decreases['CF Decreases'][i] == True:
        if decreases['Scheme'][i]=='exp':
            fc.append(cbg)
            ec.append('none')
        if decreases['Scheme'][i]=='par':
            fc.append('none')
            ec.append(cbg)
    elif decreases['Rd Decreases'][i] == True and decreases['CF Decreases'][i] == False:
        if decreases['Scheme'][i]=='exp':
            fc.append(cbr)
            ec.append('none')
        if decreases['Scheme'][i]=='par':
            fc.append('none')
            ec.append(cbr)
    else:
        print(decreases.Model[i])
        if decreases['Scheme'][i]=='exp':
            fc.append(cbb)
            ec.append('none')
        if decreases['Scheme'][i]=='par':
            fc.append('none')
            ec.append(cbb)

#%%

msize=75
alpha=0.5

pplt.rc.update(fontsize=16)
fig = pplt.figure(figsize=(8,8),sharex=True,sharey=False,tight=True)

ax = fig.subplot(111, title='RCE_'+domain+' cfv2')
for i in range(len(decreases)):
    if domain == 'large':
        ax.scatter(cf_val['305K'][i]-cf_val['295K'][i],mets['S305'][i]-mets['S295'][i],
                facecolors=fc[i], edgecolors=ec[i],marker='o',s=msize)
    ax.scatter(cf_val['305K'][i]-cf_val['295K'][i],(mets['V305'][i]-mets['V295'][i])*10,
            facecolors=fc[i], edgecolors=ec[i],marker='^',s=msize)
    ax.scatter(cf_val['305K'][i]-cf_val['295K'][i],mets['I305'][i]-mets['I295'][i],
            facecolors=fc[i], edgecolors=ec[i],marker='s',s=msize)

if domain == 'large':
    ax.scatter(-1,-1,marker='o',color='grey',label='f$_{sub}$',s=msize)
ax.scatter(-1,-1,marker='s',color='grey',label='I$_{org}$',s=msize)
ax.scatter(-1,-1,marker='^',color='grey',label='$\sigma^2_{crh}$x10',s=msize)
ax.scatter(-1,-1,marker='d',facecolor='grey',edgecolor='none',label='Explicit',s=msize)
ax.scatter(-1,-1,marker='d',facecolor='none',edgecolor='grey',label='Parameterized',s=msize)
ax.scatter(-1,-1,marker='d',facecolor=cbg,edgecolor='none',label='$\Delta$(R$_D$)<0,$\Delta$(CF)<0',s=msize)
ax.scatter(-1,-1,marker='d',facecolor=cbr,edgecolor='none',label='$\Delta$(R$_D$)<0,$\Delta$(CF)>0',s=msize)

ax.axvline(0,linestyle=':',color='grey')
ax.axhline(0,linestyle=':',color='grey')

ax.plot([-1,1],[1,-1],color='grey',linestyle='-')

if domain == 'large':
    ax.format(ylabel='$\Delta$(Aggregation)',
            xlabel='$\Delta$(Anvil Cloud Fraction)',
            grid=False,xlim=(-0.2,0.2),ylim=(-0.3,0.3))
    ax.legend(ncols=1,loc='ur')
if domain == 'small':
    ax.format(ylabel='$\Delta$(Aggregation)',
            xlabel='$\Delta$(Anvil Cloud Fraction)',
            grid=False,xlim=(-0.075,0.075),ylim=(-0.2,0.3))
    ax.legend(ncols=1,loc='ur')


if psave == 'show':
    pplt.show()
else:
    fig.savefig('stauffer2022_fig07_'+domain+'.pdf')
    pplt.close()
#%%
