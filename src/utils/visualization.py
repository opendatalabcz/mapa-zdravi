import numpy as np
import os
import matplotlib.pyplot as plt

DATA_PATH = '../../data/intermediate/'
IMAGE_PATH = '../../images/visualization/'

def study_length_info(students):
    l = []
    total_cnt = 0
    for degree in students['degree'].unique():
        dr = students[students['degree'] == degree]

        leng = dr['study_length'].unique()[0]
        print(f'Průměrná délka studia k získání titulu MUDR.: {round(np.nanmean(dr.years_for_degree),2)} let (počet ročníků studia: {leng})')
        print('Podle fakult:')
        for uni in dr['university'].unique():
            avg = round(np.nanmean(dr[dr.university == uni].years_for_degree),2)
            perc = round(100*dr[(dr.university == uni) & (dr.years_for_degree > leng) & (dr.graduated==True)].shape[0] / dr[(dr.university == uni)& (dr.graduated==True)].shape[0],2)
            total_cnt += dr[(dr.university == uni) & (dr.years_for_degree > leng)].shape[0]
            l.append([uni, avg, perc])
            print(f'   - {uni}: {avg} let (prodlužovalo: {perc} %)')

        print('----'*20)
    print(f"Celkem prodlužovalo {total_cnt}/{students[students.graduated==True].shape[0]} => {round(100*total_cnt/students[students.graduated==True].shape[0],2)} %")
    return pd.DataFrame(l, columns=['Fakulta', 'Průměrná délka studia', 'Prodloužení studia (%)'])

        
        
def get_version(name):
    files = os.listdir(IMAGE_PATH)
    return len([x for x in files if name in x])        


def save_plot(title):
    version = get_version(title)
    plt.savefig(IMAGE_PATH+title+f' v{version}.png')

