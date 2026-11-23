for x in a:cover_A_hybrid b:cover_B_mystyle; do h=${x%%:*}; o=${x##*:}
google-chrome --headless=new --no-sandbox --disable-gpu --allow-file-access-from-files --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1440 --virtual-time-budget=3000 --screenshot=$PWD/$o.png file://$PWD/$h.html 2>/dev/null; done
python3 -c "from PIL import Image;[print(f,Image.open(f).size) for f in ['cover_A_hybrid.png','cover_B_mystyle.png']]"
