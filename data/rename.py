#%%
import pandas as pd
#%%
def changerdivzunits():
    df = pd.read_csv('rdiv_large.csv',sep='\t')

    vars = ['ZGFULL295', 'ZGFULL300', 'ZGFULL305',
            'ZG300S295', 'ZG300S300', 'ZG300S305',
            'ZG300Q295', 'ZG300Q300', 'ZG300Q305']
    for i in vars:
        df[i] = df[i]/1000

    df.to_csv('rdiv_large_z.csv')

    df = pd.read_csv('rdiv_small.csv',sep='\t')

    vars = ['ZGFULL295', 'ZGFULL300', 'ZGFULL305',
            'ZG300S295', 'ZG300S300', 'ZG300S305',
            'ZG300Q295', 'ZG300Q300', 'ZG300Q305']
    for i in vars:
        df[i] = df[i]/1000

    df.to_csv('new_rdiv_small_z.csv')

def changeanvilcsvsep():
    df = pd.read_csv('small_cfv2_all.csv',sep='\t')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv('new_anvil-properties_small_cfv2.csv',sep=',')

    df = pd.read_csv('large_cfv2_all.csv',sep='\t')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv('new_anvil-properties_large_cfv2.csv',sep=',')


    df = pd.read_csv('small_cfv1_all.csv',sep='\t')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv('new_anvil-properties_small_cfv1.csv',sep=',')

    df = pd.read_csv('large_cfv1_all.csv',sep='\t')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv('new_anvil-properties_large_cfv1.csv',sep=',')

def changeraddivcsvsep():
    df = pd.read_csv('rdiv_large_z.csv')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv('new_rdiv-properties_large.csv',sep=',')

    df = pd.read_csv('rdiv_small_z.csv')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv('new_rdiv-properties_small.csv',sep=',')

def changemlsmetricscsvsep(iofile):
    df = pd.read_csv(iofile,sep='\t')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains(',')]
    df.to_csv('new_'+iofile,sep=',')

changemlsmetricscsvsep('dsea_metrics_large_exp.csv')
changemlsmetricscsvsep('javg_metrics_large_exp.csv')
changemlsmetricscsvsep('jint_metrics_large_exp.csv')
#changemlsmetricscsvsep('mlcf_metrics_large_exp.csv')
#changemlsmetricscsvsep('mlcf_metrics_large_par.csv')
#changemlsmetricscsvsep('mlsd_metrics_large_exp.csv')
#changemlsmetricscsvsep('rhum_metrics_large_exp.csv')
#changemlsmetricscsvsep('wavg_metrics_large_exp.csv')
#%%
import pandas as pd
#%%
df = pd.read_csv('rhum_metrics_large_exp.csv')
#%%
