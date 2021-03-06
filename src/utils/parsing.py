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
            faculty_df = file.parse(s_name)  # pd.read_excel(PATH_UNI + file_name)
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
    file_name_list = [file_name for file_name in os.listdir(PATH_UNI) if 'uk' in file_name]

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
    df['year_of_study'] = np.where(df['date_end'].isna(), datetime.now().year - df['date_start'], np.NaN)

    # age
    df['birth_date'] = df['date_start'] - df['age_start']
    df['age_end'] = df['age_start'] + (df['date_end'].apply(lambda x: x.year) - df['date_start'])
    df['age_now'] = df['age_start'] + (datetime.now().year - df['date_start'])

    # TODO add another features?
    return df


###########################################################
#####                 MUNI FUNCTIONS                  #####
###########################################################
def load_muni_raw():
    file_name_list = [file_name for file_name in os.listdir(PATH_UNI) if 'muni' in file_name]
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
    df['year_of_study'] = np.where(df['date_end'].isna(), datetime.now().year - df['date_start'], np.NaN)
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
    file_name_list = [file_name for file_name in os.listdir(PATH_UNI) if 'ova' in file_name]

    ova_df = __load_raws(file_name_list)
    ova_df.columns = ['major',
                      'date_end',
                      'year_of_study',
                      'citizenship',
                      'date_start',
                      'university']
    ova_df['university'] = ova_df['university'].apply(lambda x: x[:3])

    return ova_df


###########################################################
#####                 UNOB FUNCTIONS                  #####
###########################################################
def load_unob_raw():
    file_name_list = [file_name for file_name in os.listdir(PATH_UNI) if 'unob' in file_name]

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
    df['year_of_study'] = np.where(df['date_end_graduated'].isna(), datetime.now().year - df['date_start'], np.NaN)

    df = df.drop(columns=['date_end_graduated',
                          'date_end_student'])
    return df


###########################################################
#####                 UPOL FUNCTIONS                  #####
###########################################################
def load_upol_raw():
    file_name_list = [file_name for file_name in os.listdir(PATH_UNI) if 'upol' in file_name]

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
    df['year_of_study'] = np.where(~df['graduated'], datetime.now().year - df['date_start'], np.NaN)

    # age
    df['birth_date'] = df['date_start'] - df['age_start']
    df['age_end'] = df['age_start'] + (df['date_end'] - df['date_start'])
    df['age_now'] = df['age_start'] + (datetime.now().year - df['date_start'])
    
    df['university'] = df['university'].apply(lambda x: x[:4]) 
    return df

###########################################################


def country_code(name):
    d = {
    '??esk?? republika' : 'CZE',
    'Slovensko' : 'SVK',
    'Kolumbie' : 'COL',
    'Srbsko' : 'SRB',
    'Bulharsko' : 'BGR',
    'Kuvajt' : 'KWT',
    'Ukrajina' : 'UKR',
    'B??lorusko' : 'BLR',
    'Rusko' : 'RUS',
    'Kazachst??n' : 'KAZ',
    'Polsko' : 'POL',
    'Rumunsko' : 'ROU',
    'Slovensk?? republika' : 'SVK',
    'Kanada' : 'CAN',
    'Rusk?? federace' : 'RUS',
    'Spojen?? st??ty americk??' : 'USA',
    'Vietnamsk?? socialistick?? republika' : 'VNM',
    'Republika T??d??ikist??n' : 'TJK',
    'Malajsie' : 'MYS',
    'Portugalsk?? republika' : 'PRT',
    'Spojen?? kr??lovstv?? Velk?? Brit??nie a Severn??ho Irska' : 'GBR',
    '????nsk?? republika (Tchaj-wan)' : 'TWN',
    'Nov?? Z??land' : 'NZE',
    'Indick?? republika' : 'IRL',
    'Spolkov?? republika N??mecko' : 'GER',
    'Ghansk?? republika' : 'GHA',
    'Singapursk?? republika' : 'SGP',
    'Japonsko' : 'JAP',
    'Indon??sk?? republika' : 'IND',
    'Ma??arsko' : 'HUN',
    'Polsk?? republika' : 'POL',
    'Republika Kazachst??n' : 'KAZ',
    'Sa??dsk?? Ar??bie' : 'SAU',
    'Egypt' : 'EGY',
    'Kypr' : 'CYP',
    'Spojen?? st??ty' : 'USA',
    'Izrael' : 'ISR',
    'Jord??nsko' : 'JOR',
    'Velk?? Brit??nie' : 'GBR',
    'Thajsko' : 'THA',
    'Banglad????': 'BGD',
    'Indie': 'IND',
    'S??d??n': 'SDN',
    '??r??n': 'IRN',
    'Ir??k': 'IRQ',
    'S??rie': 'SYR',
    'It??lie': 'ITA',
    'Norsko': 'NOR',
    'D??nsko': 'DNK',
    'N??mecko': 'GER',
    '??v??dsko': 'SWE',
    'Portugalsko': 'PRT',
    '??r?? Lanka': 'LKA',
    'Braz??lie': 'BRA',
    'Korejsk?? republika': 'KOR',
    'Filip??ny': 'PHL',
    '??ecko': 'GRE',
    '????na': 'PRC',
    'Francie': 'FRA',
    'Gruzie': 'GEO',
    'Libanon': 'LBN',
    'Bosna a Hercegovina': 'BIH',
    'Tunisko': 'TUN',
    'Austr??lie': 'AUS',
    '??pan??lsko': 'ESP',
    'Kostarika': 'CRI',
    'Irsko': 'IRL',
    'Ji??n?? Afrika': 'JAR',
    'Etiopie': 'ETH',
    'Uzbekist??n': 'UZB',
    'P??kist??n': 'PAK',
    'Kyrgyzst??n': 'KGZ',
    'Nig??rie': 'NGA',
    'Angola': 'ANG',
    'Mexiko': 'MEX',
    'Estonsko': 'EST',
    'Rakousko': 'AUT',
    'St??t Izrael': 'ISR',
    'Nigerijsk?? federativn?? republika': 'NGA',
    '??pan??lsk?? kr??lovstv??': 'ESP',
    'P??kist??nsk?? isl??msk?? republika': 'PAK',
    'Francouzsk?? republika': 'FRA',
    'Kypersk?? republika' : 'CYP',
    'Italsk?? republika' : 'ITA',
    '??v??dsk?? kr??lovstv??' : 'SWE',
    'Egyptsk?? arabsk?? republika' : 'EGY',
    'Nizozemsko' : 'NLD',
    'Kr??lovstv?? Sa??dsk?? Ar??bie' : 'SAU',
    'Jord??nsk?? h????imovsk?? kr??lovstv??' : 'JOR',
    'Tureck?? republika' : 'TUR',
    '??r??nsk?? isl??msk?? republika' : 'IRN',
    'Ir??ck?? republika' : 'IRQ',
    'Gibraltar' : 'GBR',
    'Australsk?? spole??enstv??' : 'AUS',
    'Litevsk?? republika' : 'LTU',
    'Hondurask?? republika' : 'HND',
    'Belgick?? kr??lovstv??' : 'BEL',
    'Islandsk?? republika' : 'ISL',
    'Norsk?? kr??lovstv??' : 'NOR',
    'Salvadorsk?? republika' : 'SLV',
    'Chorvatsko' : 'HRV',
    'Spojen?? arabsk?? emir??ty' : 'ARE',
    'D??nsk?? kr??lovstv??' : 'DNK',
    'Libanonsk?? republika' : 'LBN',
    'Palestinsk?? autonomn?? ??zem??' : 'PSE',
    '????nsk?? lidov?? republika' : 'PRC',
    'Republika Uzbekist??n' : 'UZB',
    'Bahrajn' : 'BHR',
    'Zimbabwe' : 'ZWE',
    'Ghana' : 'GHA',
    'Botswana' : 'BWA',
    'Kamerun' : 'CMR',
    'Tchaj-wan' : 'TWN',
    'Malta' : 'MLT',
    'Trinidad a Tobago' : 'TTO',
    'Libye' : 'LBY',
    'Island' : 'ISL',
    'Vietnam' : 'VNM',
    'Finsko' : 'FIN',
    '??v??carsko' : 'SWI',
    'Afgh??nist??n' : 'AFG',
    'Zambie' : 'ZMB',
    'Palestina' : 'PSE',
    'Loty??sko' : 'LAT'
    
    }
    return d.get(name)