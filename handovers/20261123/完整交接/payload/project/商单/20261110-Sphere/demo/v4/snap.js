const puppeteer=require('puppeteer-core');
(async()=>{
 const times=process.argv.slice(3).map(Number), out=process.argv[2];
 const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--allow-file-access-from-files','--disable-web-security','--font-render-hinting=none','--force-color-profile=srgb']});
 const p=await b.newPage();await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 p.on('console',m=>console.log('PAGE',m.text()));p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+__dirname+'/index.html');await p.evaluate(()=>document.fonts.ready);
 await new Promise(r=>setTimeout(r,300));
 for(const t of times){await p.evaluate(t=>window.seek(t),t);await p.screenshot({path:`${out}/t_${t.toFixed(2)}.jpg`,type:'jpeg',quality:90});}
 if(process.env.META) console.log(JSON.stringify(await p.evaluate(()=>window.META)));
 await b.close();})();
