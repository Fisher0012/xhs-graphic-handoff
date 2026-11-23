from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import numpy as np,json,shutil
P=Path(__file__).resolve().parents[1]
files=sorted((P/'final').glob('0[0-3]_*.png'))
font=ImageFont.truetype('/home/box/.fonts/NotoSansSC-Medium.otf',23)
for f in files:
 im=Image.open(f).convert('RGB');assert im.size==(2160,2880)
 im.resize((400,533),Image.Resampling.LANCZOS).save(P/'evidence'/(f.stem+'_400.png'))
for w,h,name in [(400,533,'四图400px总览.png'),(800,1067,'07_总览.png')]:
 c=Image.new('RGB',(w*2,h*2),'#07090d')
 for i,f in enumerate(files):c.paste(Image.open(f).resize((w,h),Image.Resampling.LANCZOS),(i%2*w,i//2*h))
 c.save(P/('evidence' if w==400 else 'final')/name)
refs=[Image.open('/workspace/xhs/notes/20261113-大号-英伟达持股/final_v2/00_封面.png'),Image.open('/workspace/xhs/notes/20261113-大号-英伟达持股/final_v2/02_辞职与股份.png')]
for i,f in enumerate(files):
 c=Image.new('RGB',(1600,1107),'#11141a');d=ImageDraw.Draw(c);d.text((20,5),'真实英伟达已通过模板',font=font,fill='#dfe6ee');d.text((820,5),'本期 '+f.stem,font=font,fill='#dfe6ee');c.paste(refs[0 if i==0 else 1].resize((800,1067),Image.Resampling.LANCZOS),(0,40));c.paste(Image.open(f).resize((800,1067),Image.Resampling.LANCZOS),(800,40));c.save(P/'evidence'/('模板对比_%02d.png'%i))
old=Image.open(P/'evidence/before_t90/00_封面.png').convert('RGB');new=Image.open(files[0]).convert('RGB');z=np.asarray(ImageChops.difference(old,new));ch=np.any(z!=0,axis=2);allowed=np.zeros(ch.shape,dtype=bool);allowed[994:1876,86:854]=True;allowed[2680:2844,:]=True
out={'changed_pixels':int(ch.sum()),'outside_photo_and_credit':int((ch&~allowed).sum()),'allowed_regions_2x':[[86,994,854,1876],[0,2680,2160,2844]]};(P/'evidence/封面最小改动像素检查.json').write_text(json.dumps(out,indent=2));assert out['outside_photo_and_credit']==0
c=Image.new('RGB',(1600,1107),'#11141a');d=ImageDraw.Draw(c);d.text((20,5),'改前：侧脸仰头',font=font,fill='#dfe6ee');d.text((820,5),'改后：换用近正面真人照片',font=font,fill='#dfe6ee');c.paste(old.resize((800,1067),Image.Resampling.LANCZOS),(0,40));c.paste(new.resize((800,1067),Image.Resampling.LANCZOS),(800,40));c.save(P/'evidence/封面人物改前后.png');shutil.copy2(files[0],P/'cover/00_封面.png');print(out)
