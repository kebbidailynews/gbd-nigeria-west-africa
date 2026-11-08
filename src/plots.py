from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

def plot_country_trends(df: pd.DataFrame,outdir: str|Path):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    focus=df[(df.location=="Nigeria") & df.measure.isin(["DALYs","YLLs","YLDs"]) & (df.metric.str.lower()=="rate")]
    outputs=[]
    for measure,g in focus.groupby("measure"):
        fig,ax=plt.subplots(figsize=(9,5.5))
        for cause,cg in g.groupby("cause"):
            cg=cg.sort_values("year"); ax.plot(cg.year,cg.value,linewidth=1.8,label=str(cause))
            if {"lower","upper"}.issubset(cg.columns): ax.fill_between(cg.year,cg.lower,cg.upper,alpha=.12)
        ax.set(title=f"Nigeria: {measure} rates over time",xlabel="Year",ylabel="Rate (source-defined units)")
        ax.grid(alpha=.25); ax.legend(fontsize=7,frameon=False,loc="best")
        fig.tight_layout(); path=outdir/f"nigeria_{measure.lower()}_trend.png"
        fig.savefig(path,dpi=300,bbox_inches="tight"); plt.close(fig); outputs.append(str(path))
    return outputs
