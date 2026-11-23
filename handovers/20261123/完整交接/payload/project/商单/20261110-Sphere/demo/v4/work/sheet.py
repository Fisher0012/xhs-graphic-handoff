import sys,glob
from PIL import Image,ImageDraw,ImageFont
fs=sorted(glob.glob(sys.argv[1]+'/*.jpg'),key=lambda f:float(f.split('t_')[-1][:-4]))
cols=int(sys.argv[3]) if len(sys.argv)>3 else 6; w,h=360,640
rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*(h+30)),'white');d=ImageDraw.Draw(S)
fnt=ImageFont.truetype('/home/box/.fonts/NotoSansSC-Medium.otf',22)
for i,f in enumerate(fs):
  im=Image.open(f).resize((w,h));x,y=(i%cols)*w,(i//cols)*(h+30);S.paste(im,(x,y+30));d.text((x+6,y+2),f.split('t_')[-1][:-4]+'s',fill='black',font=fnt)
S.save(sys.argv[2],quality=88)
