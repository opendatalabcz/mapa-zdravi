import pandas as pd
import numpy as np
import os
from datetime import datetime

PATH_UNI = '../../data/raw/uni/'


###########################################################
#####               GENERAL FUNCTIONS                 #####
###########################################################

def __load_raws(lst):
    df = pd.DataFrame()
    for file_name in lst:
        file = pd.ExcelFile(PATH_UNI + file_name)

        for s_name in file.sheet_names:
            # pd.read_excel(PATH_UNI + file_name)
            faculty_df = file.parse(s_name)
            faculty_df['university'] = file_name.split('.')[0]
            if len(file.sheet_names) > 1:
                faculty_df['sheet'] = s_name
            df = df.append(faculty_df)
    df = df.reset_index(drop=True)
    return df


def load_raws(lst):
    return __load_raws(lst)


def __load_raw_sheets(lst, sheet_name):
    df = pd.DataFrame()
    for file_name in lst:
        faculty_df = pd.read_excel(PATH_UNI + file_name, sheet_name=sheet_name)
        faculty_df['university'] = file_name.split('.')[0]
        df = df.append(faculty_df)
    df = df.reset_index(drop=True)
    return df


###########################################################
#####                  UK FUNCTIONS                   #####
###########################################################
def load_uk_raw():
    file_name_list = [file_name for file_name in os.listdir(
        PATH_UNI) if 'uk' in file_name]

    uk_df = __load_raws(file_name_list)
    uk_df = uk_df.drop(columns=['fak.kod',
                                'fakulta',
                                'specializace',
                                'obor SIMS kod'  # CZ code for student
                                ])
    uk_df.columns = [
        'major',
        'date_end',
        'date_start',
        'age_start',
        'relevance_date',
        'university'
    ]

    return uk_df


def enrich_uk(df):
    # change column type
    df['date_end'] = pd.to_datetime(df['date_end'])
    df['relevance_date'] = pd.to_datetime(df['relevance_date'])
    df['date_start'] = pd.to_numeric(df['date_start'].apply(lambda x: x[:4]))

    # if already graduated or year of studies
    df['graduated'] = ~df['date_end'].isna()
    df['year_of_study'] = np.where(df['date_end'].isna(
    ), datetime.now().year - df['date_start'], np.NaN)

    # age
    df['birth_date'] = df['date_start'] - df['age_start']
    df['age_end'] = df['age_start'] + \
        (df['date_end'].apply(lambda x: x.year) - df['date_start'])
    df['age_now'] = df['age_start'] + (datetime.now().year - df['date_start'])

    # TODO add another features?
    return df


###########################################################
#####                 MUNI FUNCTIONS                  #####
###########################################################
def load_muni_raw():
    file_name_list = [file_name for file_name in os.listdir(
        PATH_UNI) if 'muni' in file_name]
    df = __load_raws(file_name_list)

    df.columns = [
        'degree',
        'major',
        'date_start',
        'date_end',
        'birth_date',
        'citizenship',
        'university'
    ]
    return df


def enrich_muni(df):
    # if already graduated or year of studies
    df['graduated'] = ~df['date_end'].isna()
    df['year_of_study'] = np.where(df['date_end'].isna(
    ), datetime.now().year - df['date_start'], np.NaN)
    # age
    df['age_start'] = df['date_start'] - df['birth_date']
    df['age_end'] = df['date_end'].apply(lambda x: x.year) - df['birth_date']
    df['age_now'] = datetime.now().year - df['birth_date']
    df['relevance_date'] = pd.to_datetime('06-01-2022')

    # TODO add another features?
    return df


###########################################################
#####                 OVA FUNCTIONS                   #####
###########################################################
def load_ova_raw():
    file_name_list = [file_name for file_name in os.listdir(
        PATH_UNI) if 'ova' in file_name]

    ova_df = __load_raws(file_name_list)
    ova_df.columns = ['major',
                      'date_start',
                      'date_end',
                      'citizenship',
                      'university',
                      'year_of_study']
    ova_df['university'] = ova_df['university'].apply(lambda x: x[:3])

    return ova_df


###########################################################
#####                 UNOB FUNCTIONS                  #####
###########################################################
def load_unob_raw():
    file_name_list = [file_name for file_name in os.listdir(
        PATH_UNI) if 'unob' in file_name]

    unob_df = __load_raws(file_name_list)

    unob_df.columns = [
        'graduated',
        'age_start',
        'citizenship',
        'major',
        'date_start',
        'date_end_graduated',
        'date_end_student',
        'university'
    ]
    return unob_df


def enrich_unob(df):
    df['age_start'] = df['age_start'].apply(round)

    # dates
    df['date_end'] = np.where(df['date_end_graduated'].isna(), df['date_end_student'], df['date_end_graduated']).astype(
        int)
    df['relevance_date'] = pd.to_datetime('17-01-2022')
    df['date_start'] = pd.to_numeric(df['date_start'].apply(lambda x: x[:4]))

    # age
    df['birth_date'] = df['date_start'] - df['age_start']
    df['age_end'] = df['age_start'] + (df['date_end'] - df['date_start'])
    df['age_now'] = df['age_start'] + (datetime.now().year - df['date_start'])

    # # if already graduated or year of studies
    df['graduated'] = df['graduated'] == 'Absolvent'
    df['year_of_study'] = np.where(df['date_end_graduated'].isna(
    ), datetime.now().year - df['date_start'], np.NaN)

    df = df.drop(columns=['date_end_graduated',
                          'date_end_student'])
    return df


###########################################################
#####                 UPOL FUNCTIONS                  #####
###########################################################
def load_upol_raw():
    file_name_list = [file_name for file_name in os.listdir(
        PATH_UNI) if 'upol' in file_name]

    upol_df = __load_raws(file_name_list)
    upol_df = upol_df.drop(columns=['PORADI',
                                    'STUDIJNI_OBOR',
                                    'VEK_PRI_ZAPISU.1',
                                    'Unnamed: 12',
                                    'Unnamed: 13'])

    upol_df.columns = [
        'date_start',
        'age_start',
        'citizenship',
        'major',
        'major_number',
        'language',
        'permanent_address',
        'study_length',
        'degree',
        'date_end',
        # 'age_start',
        'university',
        'gender'
    ]

    return upol_df


def enrich_upol(df):
    df['date_end'] = pd.to_numeric(df['date_end'].apply(lambda x: str(x)[-4:]))
    df['relevance_date'] = pd.to_datetime('09-12-2021')
    df['date_start'] = pd.to_numeric(df['date_start'].apply(lambda x: x[:4]))

    # if already graduated or year of studies
    df['graduated'] = np.where(df.university == 'upol_grad', True, False)
    df['year_of_study'] = np.where(
        ~df['graduated'], datetime.now().year - df['date_start'], np.NaN)

    # age
    df['birth_date'] = df['date_start'] - df['age_start']
    df['age_end'] = df['age_start'] + (df['date_end'] - df['date_start'])
    df['age_now'] = df['age_start'] + (datetime.now().year - df['date_start'])

    df['university'] = df['university'].apply(lambda x: x[:4])
    return df

###########################################################


def country_code(name):
    d = {
        'Česká republika': 'CZE',
        'Slovensko': 'SVK',
        'Kolumbie': 'COL',
        'Srbsko': 'SRB',
        'Bulharsko': 'BGR',
        'Kuvajt': 'KWT',
        'Ukrajina': 'UKR',
        'Bělorusko': 'BLR',
        'Rusko': 'RUS',
        'Kazachstán': 'KAZ',
        'Polsko': 'POL',
        'Rumunsko': 'ROU',
        'Slovenská republika': 'SVK',
        'Kanada': 'CAN',
        'Ruská federace': 'RUS',
        'Spojené státy americké': 'USA',
        'Vietnamská socialistická republika': 'VNM',
        'Republika Tádžikistán': 'TJK',
        'Malajsie': 'MYS',
        'Portugalská republika': 'PRT',
        'Spojené království Velké Británie a Severního Irska': 'GBR',
        'Čínská republika (Tchaj-wan)': 'TWN',
        'Nový Zéland': 'NZE',
        'Indická republika': 'IRL',
        'Spolková republika Německo': 'GER',
        'Ghanská republika': 'GHA',
        'Singapurská republika': 'SGP',
        'Japonsko': 'JAP',
        'Indonéská republika': 'IND',
        'Maďarsko': 'HUN',
        'Polská republika': 'POL',
        'Republika Kazachstán': 'KAZ',
        'Saúdská Arábie': 'SAU',
        'Egypt': 'EGY',
        'Kypr': 'CYP',
        'Spojené státy': 'USA',
        'Izrael': 'ISR',
        'Jordánsko': 'JOR',
        'Velká Británie': 'GBR',
        'Thajsko': 'THA',
        'Bangladéš': 'BGD',
        'Indie': 'IND',
        'Súdán': 'SDN',
        'Írán': 'IRN',
        'Irák': 'IRQ',
        'Sýrie': 'SYR',
        'Itálie': 'ITA',
        'Norsko': 'NOR',
        'Dánsko': 'DNK',
        'Německo': 'GER',
        'Švédsko': 'SWE',
        'Portugalsko': 'PRT',
        'Šrí Lanka': 'LKA',
        'Brazílie': 'BRA',
        'Korejská republika': 'KOR',
        'Filipíny': 'PHL',
        'Řecko': 'GRE',
        'Čína': 'PRC',
        'Francie': 'FRA',
        'Gruzie': 'GEO',
        'Libanon': 'LBN',
        'Bosna a Hercegovina': 'BIH',
        'Tunisko': 'TUN',
        'Austrálie': 'AUS',
        'Španělsko': 'ESP',
        'Kostarika': 'CRI',
        'Irsko': 'IRL',
        'Jižní Afrika': 'JAR',
        'Etiopie': 'ETH',
        'Uzbekistán': 'UZB',
        'Pákistán': 'PAK',
        'Kyrgyzstán': 'KGZ',
        'Nigérie': 'NGA',
        'Angola': 'ANG',
        'Mexiko': 'MEX',
        'Estonsko': 'EST',
        'Rakousko': 'AUT',
        'Stát Izrael': 'ISR',
        'Nigerijská federativní republika': 'NGA',
        'Španělské království': 'ESP',
        'Pákistánská islámská republika': 'PAK',
        'Francouzská republika': 'FRA',
        'Kyperská republika': 'CYP',
        'Italská republika': 'ITA',
        'Švédské království': 'SWE',
        'Egyptská arabská republika': 'EGY',
        'Nizozemsko': 'NLD',
        'Království Saúdská Arábie': 'SAU',
        'Jordánské hášimovské království': 'JOR',
        'Turecká republika': 'TUR',
        'Íránská islámská republika': 'IRN',
        'Irácká republika': 'IRQ',
        'Gibraltar': 'GBR',
        'Australské společenství': 'AUS',
        'Litevská republika': 'LTU',
        'Honduraská republika': 'HND',
        'Belgické království': 'BEL',
        'Islandská republika': 'ISL',
        'Norské království': 'NOR',
        'Salvadorská republika': 'SLV',
        'Chorvatsko': 'HRV',
        'Spojené arabské emiráty': 'ARE',
        'Dánské království': 'DNK',
        'Libanonská republika': 'LBN',
        'Palestinská autonomní území': 'PSE',
        'Čínská lidová republika': 'PRC',
        'Republika Uzbekistán': 'UZB',
        'Bahrajn': 'BHR',
        'Zimbabwe': 'ZWE',
        'Ghana': 'GHA',
        'Botswana': 'BWA',
        'Kamerun': 'CMR',
        'Tchaj-wan': 'TWN',
        'Malta': 'MLT',
        'Trinidad a Tobago': 'TTO',
        'Libye': 'LBY',
        'Island': 'ISL',
        'Vietnam': 'VNM',
        'Finsko': 'FIN',
        'Švýcarsko': 'SWI',
        'Afghánistán': 'AFG',
        'Zambie': 'ZMB',
        'Palestina': 'PSE',
        'Lotyšsko': 'LAT'

    }
    return d.get(name)
