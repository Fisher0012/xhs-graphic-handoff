import asyncio, json, edge_tts, sys
L = {
 "L1":"做知识口播，最难的不是内容，是出镜。",
 "L2":"架灯、调机位、录上十几遍，",
 "L3":"再熬夜剪辑、配字幕。",
 "L4":"换个做法：内容你来写，出镜交给数字人。",
 "L5":"在Sphere里导入文案，贴上稿子；",
 "L6":"选一个公共数字形象；",
 "L7":"确认生成，几分钟就出片。",
 "L8":"口型、字幕，全是自动的。",
}
async def go(k,t):
    c = edge_tts.Communicate(t, "zh-CN-YunxiNeural", boundary="WordBoundary")
    wb=[]
    with open(k+".mp3","wb") as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"].endswith("Boundary"):
                wb.append([ch["offset"]/1e7, (ch["offset"]+ch["duration"])/1e7, ch["text"]])
    json.dump(wb, open(k+".json","w"), ensure_ascii=False)
async def main():
    ks = sys.argv[1:] or list(L)
    for k in ks: await go(k,L[k])
asyncio.run(main())
