import glob
import argparse
import pandas as pd
import shutil
import os
def strip_spaces(a_str_with_spaces):
    return a_str_with_spaces.replace(' ', '')
parser = argparse.ArgumentParser()
parser.add_argument("--sector",type=int,required=True)
parser.add_argument("--bursttab", type=str)
args = parser.parse_args()

fulldat = pd.read_csv(args.bursttab,converters={'GCN Name': strip_spaces})
dat = fulldat[(fulldat["TESS Sector"]==int(args.sector)) & (fulldat["Enclosed Probability"] > 0)].copy(deep=True)
dat['GCN Name'] = dat['GCN Name'].fillna('')
dat.loc[dat["GCN Name"]=="","GCN Name"]=dat.loc[dat["GCN Name"]=="","Fermi Name"]
cwd = os.getcwd()
for val in dat['GCN Name']:
    numflag = 0
    nummult = 0
    numsingle = 0
    plotfiles = glob.glob("*jpg")
    flagfiles = []
    singlefiles = []
    multfiles = []
    for p in plotfiles:
        if val in p:
           basefile = p.split("/")[-1]
           LCtype = p.split("/")[-1].split("_")[0]
           if LCtype=="flag":
               numflag+=1
               flagfiles.append(basefile)
           elif LCtype=="single":
               numsingle+=1
               singlefiles.append(basefile)
           elif LCtype=="lc":
               nummult+=1
               multfiles.append(basefile)
           else:
               raise Exception(f"Unhandled LCtype: {LCtype}")
    if (numflag+nummult+numsingle)>0:
        htmlsummary = f"""<html>
    <! -- -->
    
    <head>
    <title></title>
    <body bgcolor="#ffffff">
    <h2>{val} Candidates</h1></body>

    <a href={val}multipleplots.html>{nummult} multi-point candidates</a>
    <br>
    <a href={val}singleplots.html>{numsingle} single-point candidates (less likely)</a>
    <br>
    <a href={val}flagplots.html>{numflag} flagged candidates</a>
    
    </html>    
"""
        with open(f"{val}resultssummary.html","w") as f:
            f.write(htmlsummary)
        htmlmult = f"""<html>
    <! -- -->
    
    <head>
    <title>Multi-point Candidates</title>
    <body bgcolor="#ffffff">
    <h2>{val}</h1></body>"""
        for mf in multfiles:
            htmlmult += f"""mf\n"""
            htmlmult += f"""<img src={mf}>\n"""
        htmlmult += """</html>"""
        htmlsingle = f"""<html>
    <! -- -->
    
    <head>
    <title>Single Point Candidates</title>
    <body bgcolor="#ffffff">
    <h2>{val} Single Point</h1></body>"""
        for sf in singlefiles:
            htmlsingle += f"""{sf}\n"""
            htmlsingle += f"""<img src={sf}>\n"""
        htmlsingle += """</html>"""
        htmlflag = f"""<html>
    <! -- -->
    
    <head>
    <title>Flagged Candidates</title>
    <body bgcolor="#ffffff">
    <h2>{val} Flagged Candidates</h1></body>"""
        for ff in flagfiles:
            htmlflag += f"""ff\n"""
            htmlflag += f"""<img src={ff}>\n"""
        htmlflag += """</html>"""
        with open(f"{val}multipleplots.html","w") as f:
            f.write(htmlmult)
        with open(f"{val}singleplots.html","w") as f:
            f.write(htmlsingle)
        with open(f"{val}flagplots.html","w") as f:
            f.write(htmlflag)
        
    
    
