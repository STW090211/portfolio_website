# Load data from raw/ and manual data to portfolio.db
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///../portfolio.db')

schizo = pd.read_excel('../raw/schizo.xls') 
schizo.to_sql('Schizo', engine, if_exists='replace', index=False)

soil = pd.read_table('../raw/soil.txt', header=None)
soil.to_sql('Soil', engine, if_exists='replace', index=False)

lamb = pd.DataFrame(
    {'Lamb': [1,2,3,4,5,6,7,8],
     'Before': [0.095, 0.106, 0.082, 0.152, 0.090, 0.086, 0.137, 0.121],
     'After': [0.176, 0.142, 0.194, 0.136, 0.115, 0.084, 0.103, 0.189]
    })
lamb.to_sql('Lamb', engine, if_exists='replace', index=False)

dice = pd.DataFrame(
    {'Face': [1,2,3,4,5,6],
     'Frequency': [30,25,35,25,20,15]
    })
dice.to_sql('Dice', engine, if_exists='replace', index=False)

pol_aff = pd.DataFrame(
    {'Gender': ['Male','Male','Male','Female','Female','Female'],
     'Affiliation': ['Democrat', 'Republican', 'Independent', 'Democrat', 'Republican', 'Independent'],
     'Frequency': [68, 56, 32, 52, 72, 20]
    })
pol_aff.to_sql('Political_Affiliation', engine, if_exists='replace', index=False)

he_color = pd.DataFrame(
{'EyeColor': ['Brown','Brown','Brown','Brown','Green/Gray', 'Green/Gray','Green/Gray','Green/Gray', 'Blue', 'Blue','Blue','Blue'],
 'HairColor': ['Brown','Black', 'Blond', 'Red','Brown','Black', 'Blond', 'Red','Brown','Black', 'Blond', 'Red'],
 'Frequency': [438, 288, 115, 16, 1387, 746, 946, 53, 807, 189, 1768, 47],
 })
he_color.to_sql('Hair_Eye_Color', engine, if_exists='replace', index=False)

tree = pd.read_csv('../raw/Tree_Data.csv', usecols=['Event','Light_ISF','AMF','Phenolics','NSC','Lignin','Time',])
tree.to_sql('Tree', engine, if_exists='replace', index=False)

orange_pulp = pd.DataFrame(
    {'trt': [1,1,1,2,2,2,3,3,3,4,4,4],
     'mc': [80.5, 79.3, 79.0, 89.1, 75.7, 81.2, 77.8, 79.5, 77.0, 76.7, 77.2, 78.6]
    })
orange_pulp.to_sql('OrangePulp', engine, if_exists='replace', index=False)

alb = pd.DataFrame(
    {'trt': [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3],
     'deg': [140, 138, 140, 138, 142, 140, 150, 120, 128, 130, 118, 130, 128, 118, 118]
    })
alb.to_sql('Alb', engine, if_exists='replace', index=False)


