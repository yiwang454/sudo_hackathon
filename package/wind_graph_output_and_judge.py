import numpy as np
import requests
import re 
import matplotlib
import matplotlib.pyplot as plt
import datetime

date = str(datetime.datetime.now())
end_date = date[0:10]
start_date2 = end_date
day =str(int(end_date[9])-1)
start_date = start_date2.replace(start_date2[9],day)
page_number = 1
result_list =[]
wind_speed = []
myToken = '5d1c9cbab2c13977a828535be6a868fd60882450'
head = {'Authorization':'token {}'.format(myToken)}

for page_number in range (1,25):
    myUrl =  'https://met.kisanhub.com/api/v2.0/sensor-data/?end_date=%s&gateway_slug=6994e966-7598-404b-980b-e2a6b7eb737b&gateway_slug=6994e966-7598-404b-980b-e2a6b7eb737b&gateway_slug=6994e966-7598-404b-980b-e2a6b7eb737b&page=%d&start_date=%s'%(end_date,page_number,start_date)
    querystring = {"start_date":start_date,"end_date":end_date,"gateway_slug":"1d074946-09d8-403d-a7e2-62ca93b41cd2"}
    response = requests.get(myUrl, headers=head,params = querystring)
    results = response.text
    pattern = re.compile('wind_speed":(\d+[.]{1}\d+)')
    groups = pattern.findall(results)
    result_list.append(groups)

for i in range (0,len(result_list)):
    for item in result_list[i]:
        wind_speed.append(float(item))

num_points = len(wind_speed)
print(num_points)

time = np.linspace(0, 0.25*num_points, num=num_points)
f = plt.figure()
plt.plot(time[-80:],wind_speed[-80:])
plt.xlabel('$time(hours)$')
plt.ylabel('$wind peed(mph)$')
plt.plot(np.unique(time[-20:]), np.poly1d(np.polyfit(time[-20:], wind_speed[-20:], 2))(np.unique(time[-20:])))

f.savefig('windspeed%d.pdf'%1)
def wind_prediction():
    '''
    Here a variable of station slug as parameter should be added
    '''
    p_coeff = np.polyfit(time[-20:],wind_speed[-20:],3)
    x3,x2,x1,x0 = p_coeff[0],p_coeff[1],p_coeff[2],p_coeff[3]
    lt = time[-1] + 2
    v_in_two = lt*lt*lt*x3+lt*lt*x2+lt*x1+x0
    print(v_in_two)
    return v_in_two
def wind_judge():
    if wind_prediction() <  7:
        return True
    else:
        return False 

wind_prediction()