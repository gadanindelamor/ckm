import json, sys
import numpy as np, networkx as nx
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
d=json.load(open(sys.argv[1])); nodes=d["nodes"]; W=np.array(d["W"]); N=len(nodes)
G=nx.Graph()
for i,n in enumerate(nodes): G.add_node(n)
for i in range(N):
  for j in range(i+1,N):
    if W[i,j]!=0: G.add_edge(nodes[i],nodes[j],w=W[i,j])
comps=sorted(nx.connected_components(G),key=len,reverse=True)
pos={}; xoff=0
for c in comps:
  sub=G.subgraph(c); p=nx.kamada_kawai_layout(sub) if len(c)>2 else nx.spring_layout(sub,seed=7)
  a=np.array(list(p.values())); a=(a-a.min(0))/(np.ptp(a,0)+1e-9)
  scale=1.0 if len(c)>8 else 0.35
  for k,(n,_) in enumerate(p.items()): pos[n]=(a[k][0]*scale*1.6+xoff, a[k][1]*scale*1.2)
  xoff+=scale*1.6+0.35
BLUE,RED,INK,MUTED,SURF="#2a78d6","#e34948","#0b0b0b","#6b6b68","#fcfcfb"
fig,ax=plt.subplots(figsize=(15,9),facecolor=SURF); ax.set_facecolor(SURF)
for u,v,dd in G.edges(data=True):
  w=dd["w"]; (x1,y1),(x2,y2)=pos[u],pos[v]
  ax.plot([x1,x2],[y1,y2],color=BLUE if w>0 else RED,ls="-" if w>0 else (0,(4,3)),lw=0.6+2.4*abs(w),alpha=.4,zorder=1)
for i,n in enumerate(nodes):
  x,y=pos[n]; ax.scatter([x],[y],s=110,marker="s" if " " in n else "o",color="white",edgecolor=INK,lw=1.3,zorder=3)
  ax.annotate(f'{i}: "{n}"',(x,y),xytext=(6,6),textcoords="offset points",fontsize=9,color=INK,zorder=4,
    bbox=dict(boxstyle="round,pad=0.15",fc=SURF,ec="none",alpha=.8))
ax.set_axis_off()
ax.set_title("Una foto de W: cada nodo es una ckm_form (la cadena) con su índice i en la lista\niap_chatroom/_state/corpus_state.json — 12 textos del canal IAP, 32 nodos, 194 acoplamientos ≠ 0",fontsize=12,color=INK,loc="left",pad=28)
h=[Line2D([],[],color=BLUE,lw=2,label="W > 0 (aparecieron juntas en textos)"),
   Line2D([],[],color=RED,lw=2,ls=(0,(4,3)),label="W < 0 (aparecieron juntas en textos con marcador de oposición)"),
   Line2D([],[],marker="o",ls="",mfc="white",mec=INK,label="forma de una palabra"),
   Line2D([],[],marker="s",ls="",mfc="white",mec=INK,label="forma de dos palabras (bigrama)")]
fig.legend(handles=h,loc="lower center",ncol=2,frameon=False,fontsize=9.5)
fig.text(0.02,0.875,"Grosor = |W|. La posición en el dibujo no significa nada: es sólo para que se lea.",ha="left",va="top",fontsize=9,color=MUTED)
plt.subplots_adjust(bottom=0.11,top=0.84,left=0.02,right=0.98)
plt.savefig(sys.argv[2],dpi=130,facecolor=SURF)
