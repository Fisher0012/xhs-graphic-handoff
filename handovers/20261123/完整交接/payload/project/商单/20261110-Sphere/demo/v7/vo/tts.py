import asyncio, json, edge_tts, sys
V="zh-CN-YunxiNeural"
# (key, text, rate, pitch)
L = [
 ("a1","做财经口播这一年多，最磨人的不是写稿，","-4%","-2Hz"),
 ("a2","是拍。","-10%","-4Hz"),
 ("b1","调灯、架机位，卡壳了还得重录；","+0%","+0Hz"),
 ("b2","录完再剪，一句句对字幕。","-2%","-1Hz"),
 ("c1","后来我换了个做法：","-6%","-2Hz"),
 ("c2","稿子自己写，出镜交给数字人。","-2%","+0Hz"),
 ("d1","在Sphere里导入文案，把稿子贴进去，","+0%","+1Hz"),
 ("d2","选一个公共数字形象，","-2%","+0Hz"),
 ("d3","确认生成，等几分钟就好。","-2%","-1Hz"),
 ("e1","字幕它自己就配好了，","-2%","+0Hz"),
 ("e2","内容还是我自己的。","-6%","-2Hz"),
]
async def go(k,t,r,p,v=V):
    c = edge_tts.Communicate(t, v, rate=r, pitch=p, boundary="WordBoundary")
    wb=[]
    with open(k+".mp3","wb") as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"].endswith("Boundary"): wb.append([ch["offset"]/1e7,(ch["offset"]+ch["duration"])/1e7,ch["text"]])
    json.dump({"text":t,"wb":wb}, open(k+".json","w"), ensure_ascii=False)
async def main():
    if sys.argv[1:]==["test"]:
        import os; os.makedirs("voice_test",exist_ok=True)
        for v in ["zh-CN-YunxiNeural","zh-CN-YunjianNeural","zh-CN-YunyangNeural"]:
            await go("voice_test/"+v.split('-')[2], L[0][1]+L[1][1], "+0%","+0Hz", v)
        return
    for k,t,r,p in L: await go(k,t,r,p)
asyncio.run(main())
