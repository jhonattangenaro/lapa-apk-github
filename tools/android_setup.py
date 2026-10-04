"""Genera íconos de la app y ajusta el manifiesto del proyecto Android recién creado."""
from PIL import Image, ImageDraw, ImageFilter
M='android/app/src/main'; R=M+'/res'
icon=Image.open('tools/lapa-icon-512.png').convert('RGBA')
dens={'mdpi':(48,108),'hdpi':(72,162),'xhdpi':(96,216),'xxhdpi':(144,324),'xxxhdpi':(192,432)}
base=Image.new('RGBA',icon.size,(32,45,52,255)); base.alpha_composite(icon)
bg=base.convert('RGB').filter(ImageFilter.GaussianBlur(50))
for d,(leg,ad) in dens.items():
    f=f'{R}/mipmap-{d}'; small=icon.resize((leg,leg),Image.LANCZOS); small.save(f'{f}/ic_launcher.png')
    m=Image.new('L',(leg,leg),0); ImageDraw.Draw(m).ellipse((0,0,leg-1,leg-1),fill=255)
    rd=Image.new('RGBA',(leg,leg),(0,0,0,0)); rd.paste(small,(0,0),m); rd.save(f'{f}/ic_launcher_round.png')
    sz=int(ad*0.64); sm=icon.resize((sz,sz),Image.LANCZOS)
    fg=Image.new('RGBA',(ad,ad),(0,0,0,0)); fg.paste(sm,((ad-sz)//2,(ad-sz)//2),sm); fg.save(f'{f}/ic_launcher_foreground.png')
    bg.resize((ad,ad),Image.LANCZOS).save(f'{f}/ic_launcher_bg.png')
for n in ('ic_launcher','ic_launcher_round'):
    open(f'{R}/mipmap-anydpi-v26/{n}.xml','w').write('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@mipmap/ic_launcher_bg"/>\n    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>')
open(f'{R}/drawable/ic_stat_lapa.xml','w').write('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M12,22c1.1,0 2,-0.9 2,-2h-4c0,1.1 0.89,2 2,2zM18,16v-5c0,-3.07 -1.64,-5.64 -4.5,-6.32V4c0,-0.83 -0.67,-1.5 -1.5,-1.5s-1.5,0.67 -1.5,1.5v0.68C7.63,5.36 6,7.92 6,11v5l-2,2v1h16v-1l-2,-2z"/></vector>')
open(f'{R}/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources><color name="ic_launcher_background">#202D34</color></resources>')
p=M+'/AndroidManifest.xml'; s=open(p).read()
if 'POST_NOTIFICATIONS' not in s:
    s=s.replace('<uses-permission android:name="android.permission.INTERNET" />','<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />\n    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />')
open(p,'w').write(s); print('Android listo')
