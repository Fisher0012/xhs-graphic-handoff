# 贴息估算：30年等额本息、3.05%、每月贴息=余额*1%/12，60期
r=0.0305/12;n=360
for P in [500000,800000,1000000]:
    pay=P*r/(1-(1+r)**-n); b=P; tot=0; first=None
    for k in range(60):
        s=b*0.01/12; first=first or s; tot+=s; b-=pay-b*r
    print(P, round(pay,2), round(first,2), round(tot))
