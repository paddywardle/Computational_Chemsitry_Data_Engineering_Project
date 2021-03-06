from HTTPRequests import HTTPRequests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import lxml
from MySQL_Database.CreateDB import CreateDB
from main.config import configuration_dict

def pubchem_compound_properties_query(num_records: int, start_cid: int=1, write_to_db: str='yes') -> int:

    if write_to_db.upper() == "YES":
    
        user = configuration_dict['user']
        password = configuration_dict['password']
        database = configuration_dict['db_name']

        # writing to MySQL database
        db_instance = CreateDB(user, password)

    # initialise HTTPRequests class
    api_class = HTTPRequests()

    # api properties
    properties = ['MolecularFormula','MolecularWeight','CanonicalSMILES','IsomericSMILES','InChI','InChIKey','IUPACName','Title','XLogP','ExactMass','MonoisotopicMass','TPSA','Complexity','Charge','HBondDonorCount','HBondAcceptorCount',
                'RotatableBondCount','HeavyAtomCount','IsotopeAtomCount','AtomStereoCount','DefinedAtomStereoCount','UndefinedAtomStereoCount','BondStereoCount','DefinedBondStereoCount','UndefinedBondStereoCount','CovalentUnitCount','Volume3D',
                'XStericQuadrupole3D','YStericQuadrupole3D','ZStericQuadrupole3D','FeatureCount3D','FeatureAcceptorCount3D','FeatureDonorCount3D','FeatureAnionCount3D','FeatureCationCount3D','FeatureRingCount3D','FeatureHydrophobeCount3D',
                'ConformerModelRMSD3D','EffectiveRotorCount3D','ConformerCount3D','Fingerprint2D']
    
    # joining them into a comma-separated string
    properties_string = ','.join(properties)

    # api url with values that can be formatted later <- iterating from starting cid to starting cid + num_records
    # because 0 isn't a record in the pubchem database
    for i in tqdm(range(start_cid, num_records+start_cid)):

        try:

            # url for properties database
            properties_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{it}/property/{properties}/XML'.format(it=i, properties=properties_string)

            # response for properties database
            properties_response = api_class.get(properties_url)

            # beautiful soup object for XML property data
            properties_bs = BeautifulSoup(properties_response.content, 'xml')

            # list to store xml tag values
            properties_data = {}

            # iterating through xml tags
            for prop in properties:
                # getting all values for each tag
                for text in properties_bs.find_all(prop):
                    b = text
                    # appending xml tag value to properties_data
                    properties_data[prop] = [b.get_text()]

            # creating dataframe from properties data (have to reshape as it is a column list)
            properties_df = pd.DataFrame(properties_data)

            # url for images database
            images_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{it}/PNG?record_type=2d&image_size=small'.format(it=i)

            # response for image database
            images_response = api_class.get(images_url)

            # images dataframe with single record
            images_df = pd.DataFrame([images_response.content], columns=['image'])

            if write_to_db.upper() == "YES":

                # writing properties dataframe to properties table in database
                db_instance.write_df('properties', database, properties_df)

                # writing image dataframe to images table in database
                db_instance.write_df('images', database, images_df)
        
        except AttributeError:

            pass

    return 0

if __name__ == "__main__":

    # record to start at in requests
    starting_record = int(input("Input record to start at: "))

    # number of records user wants
    num_records = int(input("Input the number of records you want: "))

    # write_to_db?
    write_to_db = input("Would you like to write data to the database?: ")

    # calling function
    pubchem_compound_properties_query(num_records, starting_record, write_to_db)