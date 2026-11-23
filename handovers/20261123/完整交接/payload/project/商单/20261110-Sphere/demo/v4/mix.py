import json,subprocess
m=json.load(open('meta.json'));A='../audio'
ins=['-i',f'{A}/bgm.mp3','-i',f'{A}/vo.wav','-i',f'{A}/sfx_glitch.mp3','-i',f'{A}/sfx_whoosh.mp3','-i',f'{A}/sfx_click.mp3','-i',f'{A}/sfx_tick.mp3']
D=m['DUR'];f=[];labs=[]
f.append(f"[0:a]atrim=8,asetpts=PTS-STARTPTS,atrim=0:{D},asetpts=PTS-STARTPTS,loudnorm=I=-29:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.05,afade=t=out:st={D-0.5}:d=0.5[bgm]");labs.append('[bgm]')
f.append(f"[1:a]atrim=0:{D},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11[vo]");labs.append('[vo]')
f.append("[2:a]atrim=0:0.8,asetpts=PTS-STARTPTS,volume=0.6,afade=t=out:st=0.55:d=0.2[gl]");labs.append('[gl]')
W=m['WHOOSH'];f.append(f"[3:a]atrim=0.32:0.90,asetpts=PTS-STARTPTS,asplit={len(W)}"+''.join(f'[w{i}]' for i in range(len(W))))
for i,(t,v) in enumerate(W):
  d=int(max(0,t-0.08)*1000);f.append(f"[w{i}]volume={v},adelay={d}|{d}[ww{i}]");labs.append(f'[ww{i}]')
C=m['CLICKS'];f.append(f"[4:a]volume=0.5,asplit={len(C)}"+''.join(f'[c{i}]' for i in range(len(C))))
for i,t in enumerate(C):
  d=int(t*1000);f.append(f"[c{i}]adelay={d}|{d}[cc{i}]");labs.append(f'[cc{i}]')
T=m['TICKS'];f.append(f"[5:a]volume=0.45,asplit={len(T)}"+''.join(f'[k{i}]' for i in range(len(T))))
for i,t in enumerate(T):
  d=int(t*1000);f.append(f"[k{i}]adelay={d}|{d}[kk{i}]");labs.append(f'[kk{i}]')
f.append(''.join(labs)+f"amix=inputs={len(labs)}:normalize=0:dropout_transition=0,atrim=0:{D},alimiter=limit=0.95[a]")
cmd=['ffmpeg','-v','error','-y','-framerate','30','-i','frames/f_%04d.jpg']+ins+['-filter_complex',';'.join(f)+';[0:v]format=yuv420p[v]','-map','[v]','-map','[a]','-c:v','libx264','-preset','slow','-crf','16','-profile:v','high','-movflags','+faststart','-c:a','aac','-b:a','192k','-t',str(D),'../sphere_style_demo_v4.mp4']
# fix: video is input 0; audio inputs shift by 1
fc=';'.join(f)
for k in range(5,-1,-1): fc=fc.replace(f'[{k}:a]',f'[{k+1}:a]')
cmd[cmd.index('-filter_complex')+1]=fc+';[0:v]format=yuv420p[v]'
subprocess.run(cmd,check=True)
print('done')
