const puppeteer=require('puppeteer-core');const fs=require('fs');
(async()=>{
 const out=__dirname+'/frames';fs.mkdirSync(out,{recursive:true});
 const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--allow-file-access-from-files','--disable-web-security','--font-render-hinting=none','--force-color-profile=srgb']});
 const p=await b.newPage();await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+__dirname+'/index.html');await p.evaluate(()=>document.fonts.ready);await new Promise(r=>setTimeout(r,400));
 const meta=await p.evaluate(()=>window.META);fs.writeFileSync(__dirname+'/meta.json',JSON.stringify(meta));
 const N=Math.round(meta.DUR*meta.FPS);
 for(let i=0;i<N;i++){await p.evaluate(t=>window.seek(t),i/meta.FPS);await p.screenshot({path:`${out}/f_${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:94});if(i%120==0)console.log('frame',i,'/',N);}
 await b.close();})();
