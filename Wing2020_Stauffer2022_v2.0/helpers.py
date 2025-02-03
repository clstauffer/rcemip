import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

a1,b1,c1 = np.array([[217/255,95/255,2/255,1]]),np.array([[117/255,112/255,179/255,1]]),np.array([[27/255,158/255,119/255,1]])
a2,b2,c2 = np.array( [217/255,95/255,2/255,1] ),np.array( [117/255,112/255,179/255,1] ),np.array( [27/255,158/255,119/255,1] )

def get_data(df,sst):
    s = ['C','C','A','C','A','C','A','C','C','A','A','C','A','A','A','C','A','A','A','C','C','A','C','A','A','A','A','A','C','C','C','C','C','C']
    d = {'MODEL':df.MODEL.values, 'VCRH':df['V'+sst].values, 'SUBFRAC':df['S'+sst].values, 'IORG':df['I'+sst].values,'scheme':s}
    return pd.DataFrame(d)

def calc_slope(bfdata,tt):
    bf = np.polyfit(tt,bfdata,1)
    m  = bf[0]
    return(m)

def calc_roc(df295,df300,df305,models,mtype,domain):
    aa,bb,cc = [],[],[]
    count = 0
    for i in df300.MODEL.values:
        if any(i == xxx for xxx in models):
            aa.append(calc_slope([df295[mtype][count],df300[mtype][count]],[295,300]))
            bb.append(calc_slope([df300[mtype][count],df305[mtype][count]],[300,305]))
            cc.append(calc_slope([df295[mtype][count],df300[mtype][count],df305[mtype][count]],[295,300,305]))
        else:
            aa.append(np.nan)
            bb.append(np.nan)
            cc.append(np.nan)
        count+=1

    slopes = pd.DataFrame({'MODEL':df295.MODEL,'295-300':aa,'300-305':bb,'295-305':cc,'scheme':df295.scheme})
    return(slopes)

def plot_metric_scatter(df,vtype,ylims,ylabels,axhline,title,savetitle,PTYPE='show'):

    fig = plt.figure(figsize=(30, 15))

    ax1 = plt.subplot2grid((1, 6), (0, 0), colspan=5)
    ax1.scatter(x=df.MODEL,y=df['SUBFRAC'],marker='o',s=300,c = a1,label='$f_{sub}$')

    ax2 = ax1.twinx()
    ax2.scatter(x=df.MODEL,y=df['IORG'],marker='s',s=300,c = b1,label='$I_{ORG}$')

    ax3 = ax1.twinx()
    if vtype == 'pw':
        ax3.scatter(x=df.MODEL,y=df['VCRH'],marker='^',s=300,c=c1,label='$\sigma^2_{PW/<PW>}$')
    if vtype == 'crh':
        ax3.scatter(x=df.MODEL,y=df['VCRH'],marker='^',s=300,c=c1,label='$\sigma^2_{CRH}$')

    ax2.spines['right'].set_position(('axes', 1.15))
    ax2.set_frame_on(True)
    ax2.patch.set_visible(False)

    ax3.spines['right'].set_position(('axes', 1.25))
    ax3.set_frame_on(True)
    ax3.patch.set_visible(False)

    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax3.spines['top'].set_visible(False)

    ax1.set_xlim(-1,len(df.MODEL))
    ax1.set_xticks(df.MODEL)
    ax1.set_xticklabels(labels=df.MODEL)

    ax1.tick_params(axis='x',labelrotation=90,labelsize=25)

    ax1.set_ylabel(ylabels[0],fontsize=30,color=a2)
    ax2.set_ylabel(ylabels[1],fontsize=30,color=b2)
    ax3.set_ylabel(ylabels[2],fontsize=30,color=c2)

    ax1.set_ylim(ylims[0][0],ylims[0][1])
    ax2.set_ylim(ylims[1][0],ylims[1][1])
    ax3.set_ylim(ylims[2][0],ylims[2][1])

    ax1.tick_params(axis='y',labelsize=30)#,colors=a2)
    ax2.tick_params(axis='y',labelsize=30)#,colors=b2)
    ax3.tick_params(axis='y',labelsize=30)#,colors=c2)

    ax3.axvline(16.5,linewidth=2,linestyle="--",color='grey')
    if axhline:
        ax3.axhline(0,linewidth=2,linestyle="--",color='grey')

    def plot_box(ax,pval,padd,color):
        median = np.nanmedian(pval)
        q1 = np.nanquantile(pval,.25)
        q3 = np.nanquantile(pval,.75)
        w1 = q1 - (1.5*(q3-q1))
        w3 = q3 + (1.5*(q3-q1))
        fliers = pval[np.where((pval<w1) | (pval>w3))[0]]
        if w3>np.nanmax(pval):
            w3=np.nanmax(pval)
        if w1<np.nanmin(pval):
            w1=np.nanmin(pval)

        ax.plot([0.02+padd,.1+padd],[median,median],color=color,linewidth=5)
        ax.plot([0.02+padd,.1+padd],[q1,q1],color=color,linewidth=5)
        ax.plot([0.02+padd,.1+padd],[q3,q3],color=color,linewidth=5)
        ax.plot([0.02+padd,0.02+padd],[q1,q3],color=color,linewidth=5)
        ax.plot([.1+padd,.1+padd],[q1,q3],color=color,linewidth=5)
        ax.plot([.06+padd,.06+padd],[w1,q1],color=color,linewidth=5)
        ax.plot([.06+padd,.06+padd],[q3,w3],color=color,linewidth=5)
        if len(fliers)>0:
            ax.scatter(np.ones((len(fliers)))*.06+padd,fliers,color=color,s=12)

    ax10 = plt.subplot2grid((1, 6), (0, 5), colspan=1)
    ax10.set_frame_on(False)
    plot_box(ax10,df['SUBFRAC'].values,0,a2)
    ax10.set_ylim(ylims[0][0],ylims[0][1])
    ax10.set_xlim(0,1)
    ax10.set_yticks([])
    ax10.set_xticks([])
    ax10.tick_params(axis='x',labelsize=25,labelrotation=90)

    ax11 = ax10.twinx()
    ax11.set_frame_on(False)
    plot_box(ax11,df['IORG'].values,0.15,b2)
    ax11.set_ylim(ylims[1][0],ylims[1][1])
    ax11.set_xlim(0,1)
    ax11.set_yticks([])
    ax11.set_xticks([])
    ax11.set_xticklabels([])

    ax12 = ax11.twinx()
    ax12.set_frame_on(False)
    plot_box(ax12,df['VCRH'].values,.30,c2)
    ax12.set_ylim(ylims[2][0],ylims[2][1])
    ax12.set_xlim(0,1)
    ax12.set_yticks([])

    ax12.set_xticks([0.05,0.2,0.35])
    ax12.set_xticklabels(ylabels)

    ax1.set_title(title,fontsize=54)

    fig.legend(loc=4,fontsize=30)

    plt.tight_layout()
    if PTYPE == 'save':
        plt.savefig(savetitle,bbox_inches='tight')
        plt.close()
    if PTYPE == 'show':
        plt.show()

def plot_roc_comp(subf_slopes,iorg_slopes,vcrh_slopes,vtype,savetitle,PTYPE='show'):
    # 300K-295K AND 305K-300K VALUE OF ALL METRICS, ALL MODELS
    fig,ax=plt.subplots(figsize=(35,15))
    fig.subplots_adjust(right=0.9)

    ax1 = ax
    ax2 = ax.twinx()
    ax3 = ax.twinx()

    ax3.spines['right'].set_position(('axes', 1.1))
    ax3.set_frame_on(True)
    ax3.patch.set_visible(False)

    ax1.scatter(x=np.arange(len(subf_slopes.MODEL)),y=subf_slopes['295-300'],marker='o',s=300,c=a1)
    ax2.scatter(x=np.arange(len(subf_slopes.MODEL)),y=iorg_slopes['295-300'],marker='s',s=300,color=b1)
    ax3.scatter(x=np.arange(len(subf_slopes.MODEL)),y=vcrh_slopes['295-300'],marker='^',s=300,color=c1)

    ax1.scatter(x=np.arange(len(subf_slopes.MODEL)),y=subf_slopes['300-305'],marker='o',s=300,edgecolors=a1,facecolors='none')
    ax2.scatter(x=np.arange(len(subf_slopes.MODEL)),y=iorg_slopes['300-305'],marker='s',s=300,edgecolors=b1,facecolors='none')
    ax3.scatter(x=np.arange(len(subf_slopes.MODEL)),y=vcrh_slopes['300-305'],marker='^',s=300,edgecolors=c1,facecolors='none')

    p = []

    p.append(ax1.scatter(-3,0,marker='o',s=300,c=a1,label='$f_{sub}$'))
    p.append(ax1.scatter(-3,0,marker='s',s=300,c=b1,label='$I_{ORG}$'))
    if vtype == 'pw':
        p.append(ax1.scatter(-3,0,marker='^',s=300,c=c1,label='$\sigma^2_{PW/<PW>}$'))
    if vtype == 'crh':
        p.append(ax1.scatter(-3,0,marker='^',s=300,c=c1,label='$\sigma^2_{CRH}$'))
    p.append(ax1.scatter(-3,0,marker='d',s=300,c='black',label='295K-300K'))
    p.append(ax1.scatter(-3,0,marker='d',s=300,edgecolors='black',label='300K-305K',facecolors='none'))

    ax.set_xlim(-1,len(subf_slopes.MODEL.values))
    ax.set_xticks(np.arange(len(subf_slopes.MODEL.values)))
    ax.set_xticklabels(labels=subf_slopes.MODEL.values)

    ax.tick_params(axis='x',labelrotation=90,labelsize=25)
    ax1.tick_params(axis='y',labelsize=30)#,colors=a)
    ax2.tick_params(axis='y',labelsize=30)#,colors=b)
    ax3.tick_params(axis='y',labelsize=30)#,colors=c)
    ax1.set_ylabel('$df_{sub}/dSST$',fontsize=54,color=a2)
    ax2.set_ylabel('$dI_{ORG}/dSST$',fontsize=54,color=b2)
    if vtype == 'pw':
        ax3.set_ylabel('$d\sigma^2_{PW/<PW>}/dSST$',fontsize=54,color=c2)
    if vtype == 'crh':
        ax3.set_ylabel('$d\sigma^2_{CRH}/dSST$',fontsize=54,color=c2)

    ax1.set_ylim(-0.04,0.04)
    ax2.set_ylim(-0.04,0.04)
    if vtype == 'pw':
        ax3.set_ylim(-0.025,0.025)
    if vtype == 'crh':
        ax3.set_ylim(-0.006,0.006)

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax3.spines['top'].set_visible(False)

    ax.axhline(0,linewidth=2,linestyle="--",color='grey')
    ax.axvline(16.5,linewidth=2,linestyle="--",color='grey')

    ax.set_title('Rate of Change of Large Domain Metrics',fontsize=54)

    fig.legend(handles=p,loc=4,fontsize=30)

    plt.tight_layout()
    if PTYPE == 'save':
        plt.savefig(savetitle,bbox_inches='tight')
        plt.close()
    if PTYPE == 'show':
        plt.show()
