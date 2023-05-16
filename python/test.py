import pandas as pd

address = '서울특별시 강남구 도산대로85길 56 (청담동, 현대한강아파트)'


def classCheck(jeonseMoney,seniorMoney,address,buildingType, area, floor=None): # 아파트인지 단독주택인지, 오피스텔인지 확인
    if buildingType == 'apart': #아파트
        j1 = avoJeonse(jeonseMoney,seniorMoney,address,'아파트(매매)__실거래가_20230508213822.csv')
        j1.calMoney(floor,area)
        j1.checkRisk()
    elif buildingType == 'house': #단독/다가구
        j1  = houseJeonse(jeonseMoney,seniorMoney,address,'아파트(매매)__실거래가_20230508213822.csv')
        j1.calMoney(area)
        j1.checkRisk()
    elif buildingType == 'villa': #연립/다세대
        j1 = avoJeonse(jeonseMoney,seniorMoney,address,'연립다세대(매매)__실거래가_20230515142046.csv')
        j1.calMoney(floor,area)
        j1.checkRisk()
    elif buildingType == 'officetels': #오피스텔
        j1 = avoJeonse(jeonseMoney,seniorMoney,address,'오피스텔(매매)__실거래가_20230515231738.csv')
        j1.calMoney(floor,area)
        j1.checkRisk()



class CanJeonse:
    def __init__(self,jeonseMoney,seniorMoney,address,fileName):
        self.jeonseMoney = jeonseMoney #전세값
        self.seniorMoney = seniorMoney #선순위 보증금
        self.address = address # 주소
        self.fileName = fileName #csv파일 이름
        self.actualTransaction = 0 # 실거래가

    def checkRisk(self):
        if (self.actualTransaction * 0.8) < self.jeonseMoney + self.seniorMoney:
            print('사기 위험 있습니다.')
        else:
            print('사기 위험 없습니다.')

        
    
class avoJeonse(CanJeonse): #아파트, 빌라, 오피스텔 전세        
    def calMoney(self,floor,area):
        floor = float(floor)
        df = pd.read_csv(self.fileName, encoding='cp949',thousands = ',')
        roadName = " ".join(address.split()[2:4]) #도로명 주소
        target = df.loc[df.eq(roadName).any(axis = 1)]
        if target.empty:
            self.actualTransaction = 0 # 실거래가 가져오기
        else:
            targetFloorCheck = target[target['층'] == floor]
            target = target.copy()
            target['target_money'] = (target['거래금액(만원)']  / target['전용면적(㎡)']) * area
            if (targetFloorCheck.empty):
                targetMoneyList = list(target['target_money'])
                targetMoney = (sum(targetMoneyList) / len(targetMoneyList))
            else:
                target = target[target['층'] == floor]
                targetMoneyList = list(target['target_money'])
                targetMoney = targetMoneyList[0]
            self.actualTransaction = targetMoney


class houseJeonse(CanJeonse): # 단독 주택 전세
    def calMoney(self,area):
        df = pd.read_csv(self.fileName, encoding='cp949',thousands = ',')
        roadName = " ".join(address.split()[2:4]) #도로명 주소
        target = df.loc[df.eq(roadName).any(axis = 1)]
        target = df.loc[df.eq(roadName).any(axis = 1)]
        if target.empty:
            self.actualTransaction = 0 # 실거래가 가져오기
        else:
            target = target.copy()
            target['target_money'] = (target['거래금액(만원)']  / target['대지면적(㎡)']) * area
            targetMoneyList = list(target['target_money'])
            targetMoney = (sum(targetMoneyList) / len(targetMoneyList))
            self.actualTransaction = targetMoney

        

classCheck(1,1,address,'apart',80,17)

