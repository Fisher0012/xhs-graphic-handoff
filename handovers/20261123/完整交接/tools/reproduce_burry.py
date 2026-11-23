#!/usr/bin/env python3
"""Only make relocated derivative HTML; opt-in local screenshots. No publishing."""
from pathlib import Path
import argparse,subprocess,shlex
p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--chrome',default='google-chrome');a=p.parse_args()
root=Path(__file__).resolve().parent.parent
project=root/'payload/project';fonts=root/'payload/dependencies/fonts'
note=project/'notes/20261122-大号-Burry看空与减仓'
files=[note/'cover/00_封面.html',note/'pages/01_原先为何做空.html',note/'pages/02_财报与看空逻辑.html',note/'pages/03_减仓不等于转多.html']
output=root/'reproduction'
for f in files:
 target=output/(f.stem+'.html');png=target.with_suffix('.png')
 command=[a.chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--hide-scrollbars','--force-device-scale-factor=2','--window-size=1080,1440','--virtual-time-budget=3000','--screenshot='+str(png),target.as_uri()]
 print(shlex.join(command))
 if not a.render:continue
 output.mkdir(parents=True,exist_ok=True)
 text=f.read_text().replace('/workspace/xhs/',str(project)+'/').replace('/home/box/.fonts/',str(fonts)+'/')
 target.write_text(text)
 subprocess.run(command,check=True)
 from PIL import Image
 with Image.open(png) as im:
  if im.size!=(2160,2880):raise RuntimeError('Unexpected dimensions: '+str(im.size))
