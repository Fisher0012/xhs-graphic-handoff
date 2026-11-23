import asyncio, json, edge_tts
L = {
 "L1":"不想出镜，也能做口播视频。",
 "L2":"在Sphere里，贴上文案，",
 "L3":"再挑个现成的数字人，",
 "L4":"点生成，几分钟出片。",
 "L5":"口型、字幕、配图，全自动。",
}
async def go(k,t):
    c = edge_tts.Communicate(t, "zh-CN-YunxiNeural", rate="+8%", boundary="WordBoundary")
    wb=[]
    with open(k+".mp3","wb") as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"].endswith("Boundary"):
                wb.append([ch["offset"]/1e7, (ch["offset"]+ch["duration"])/1e7, ch["text"]])
    json.dump(wb, open(k+".json","w"), ensure_ascii=False)
async def main():
    for k,t in L.items(): await go(k,t)
asyncio.run(main())
