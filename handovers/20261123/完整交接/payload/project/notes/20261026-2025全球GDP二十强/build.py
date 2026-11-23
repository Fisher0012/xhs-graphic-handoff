import json,csv,re
rows=list(csv.DictReader(open('src/weo_ngdpd.csv')))
isagg=lambda c: bool(re.match(r'^G[X0-9]',c))
imf={};imf24={};meta={}
for x in rows:
    if not x['OBS_VALUE']: continue
    if x['COUNTRY']=='G001' and x['TIME_PERIOD']=='2025': world=float(x['OBS_VALUE'])
    if isagg(x['COUNTRY']): continue
    (imf if x['TIME_PERIOD']=='2025' else imf24)[x['COUNTRY']]=float(x['OBS_VALUE'])
    meta[x['COUNTRY']]=x
c=json.load(open('src/wb_countries.json'))[1]
iso={x['id'] for x in c if x['region']['value']!='Aggregates'}
d=json.load(open('src/wb_gdp.json'))[1]
wb={x['countryiso3code']:x['value'] for x in d if x['date']=='2025' and x['value'] and x['countryiso3code'] in iso}
wr={k:i+1 for i,(k,v) in enumerate(sorted(wb.items(),key=lambda t:-t[1]))}
r=sorted(imf.items(),key=lambda t:-t[1]); r24={k:i+1 for i,(k,v) in enumerate(sorted(imf24.items(),key=lambda t:-t[1]))}
zh=dict(USA="美国",CHN="中国",DEU="德国",JPN="日本",GBR="英国",IND="印度",FRA="法国",RUS="俄罗斯",ITA="意大利",CAN="加拿大",BRA="巴西",ESP="西班牙",KOR="韩国",AUS="澳大利亚",MEX="墨西哥",TUR="土耳其",IDN="印度尼西亚",NLD="荷兰",SAU="沙特阿拉伯",CHE="瑞士",POL="波兰",TWN="中国台湾")
IMFURL="https://data.imf.org/en/datasets/IMF.RES:WEO"
API="https://api.imf.org/external/sdmx/2.1/data/IMF.RES,WEO/.NGDPD.A?startPeriod=2024&endPeriod=2025&format=csv"
WBURL="https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024:2025&format=json&per_page=2000"
out=[]
for i,(k,v) in enumerate(r[:22]):
    m=meta[k]
    out.append(dict(rank_imf_2025=i+1,iso3=k,name=zh[k],gdp_2025_usd_bn=round(v/1e9,1),gdp_2025_usd_trn=round(v/1e12,2),
      share_world_pct_自算=round(v/world*100,2),imf_latest_actual=m['LATEST_ACTUAL_ANNUAL_DATA'],value_2025_status="实际值(actual)" if m['LATEST_ACTUAL_ANNUAL_DATA'] in('2025','FY2025/26') else "估计值(estimate)",
      reporting_year=m['START_END_MONTHS_OF_REPORTING_YEAR'],imf_country_update=m['COUNTRY_UPDATE_DATE'],
      gdp_2024_usd_bn_same_edition=round(imf24[k]/1e9,1),rank_imf_2024_same_edition_自算=r24[k],
      usd_change_pct_自算=round((v/imf24[k]-1)*100,2),
      wb_2025_usd_bn=round(wb[k]/1e9,1) if k in wb else None,rank_wb_2025=wr.get(k),
      wb_vs_imf_pct_自算=round((wb[k]/v-1)*100,2) if k in wb else None))
nbs=1401879/7.1429
data=dict(title="2025年全球GDP二十强（名义美元）",generated="2026-10-26",
 imf=dict(edition="IMF World Economic Outlook, October 2026（WEO 数据流版本 IMF.RES:WEO 9.0.0）",publication_date="2026-10-13T02:00Z（北京时间10-13 10:00）",
   indicator="NGDPD 现价美元GDP",dataset_url=IMFURL,api_url=API,report_url="https://www.imf.org/en/publications/weo/issues/2026/10/13/world-economic-outlook-october-2026",
   world_2025_usd_bn=round(world/1e9,1),note="前22名经济体的LATEST_ACTUAL_ANNUAL_DATA均为2025（印度为FY2025/26，财年4月-3月），即2025为该版实际值而非预测"),
 worldbank=dict(source="World Development Indicators（sourceid 2）",indicator="NY.GDP.MKTP.CD",lastupdated="2026-10-08",api_url=WBURL,
   note="世界银行不单列中国台湾"),
 china_check=dict(nbs_gdp_2025_yi=1401879,nbs_url="https://www.stats.gov.cn/sj/zxfb/202602/t20260228_1962662.html",
   nbs_avg_rate=7.1429,nbs_rate_source="《2025年国民经济和社会发展统计公报》：全年人民币平均汇率为1美元兑7.1429元人民币",
   nbs_converted_usd_bn_自算=round(nbs/10,1),imf_usd_bn=round(imf['CHN']/1e9,1),
   wb_usd_bn=round(wb['CHN']/1e9,1),wb_lcu_yuan=140187920000000,wb_rate_PA_NUS_FCRF=7.18984737402171,
   explanation="IMF与NBS按公报平均汇率折算结果一致（差额不足0.1亿美元）；世行人民币GDP同为1401879亿元，但使用其PA.NUS.FCRF年均汇率7.1898，故折算结果为19498.0十亿美元，比IMF低约1282亿美元（-0.65%）"),
 rank_diff_imf_vs_wb_top20=["澳大利亚：IMF第14 / 世行第15","墨西哥：IMF第15 / 世行第14","其余前20名次一致；前20名单一致","中国台湾：IMF第22（不在前20），世行无单列数据"],
 economies=out)
json.dump(data,open('data.json','w'),ensure_ascii=False,indent=1)
for o in out: print(o['rank_imf_2025'],o['name'],o['gdp_2025_usd_bn'],o['share_world_pct_自算'],o['value_2025_status'],o['rank_imf_2024_same_edition_自算'],o['usd_change_pct_自算'],o['wb_2025_usd_bn'],o['rank_wb_2025'],o['wb_vs_imf_pct_自算'])
print(data['china_check'])
print('top20 share',round(sum(o['gdp_2025_usd_bn'] for o in out[:20])/(world/1e9)*100,2),'top10',round(sum(o['gdp_2025_usd_bn'] for o in out[:10])/(world/1e9)*100,2))
