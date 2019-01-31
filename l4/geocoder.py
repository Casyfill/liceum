import argparse, sys
import requests as rq
from csv import DictReader, DictWriter  # чтение csv
import time



def geocode(address:str, sleep=1, **kwargs) -> dict:
    '''geocode using nomitatim service
    
    docs: http://nominatim.org/release-docs/latest/api/Search/
    
    args:
        address(str): address to query'''
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q':address, 'format':'geojson'}
    params.update(kwargs)

    r = rq.get(url, params=params)
    r.raise_for_status()  # raise if something wrong with response
    time.sleep(sleep) # dodge nominatim's requests-per-second limits
    
    return r.json()  # requests knows how to parse json answer into dictionary 


def pull_coords(response):
    '''retreive pair of coordinates from Nominatim API response'''
    if len(response['features']) == 0:
        return None
    
    return response['features'][0]['geometry']['coordinates']
    

def _name(path:str) -> str:
    '''if no output, tweak input path'''
    I = path.rfind('.')
    return path[:I] + '_geocoded' + path[I:]


def _batch_geocode(data:list, column='address', **kwargs) -> list:
    '''return coordinate pair for each dict in a list, using {column} parameter
    '''
    
    for row in data:
        r = geocode(row[column], **kwargs)
        coords = pull_coords(r)

        row['lat'], row['lon'] = coords
    return data


def store_csv(data, path):
    '''stores csv assuming data is a list of dicts, all with the same keys'''
    with open(path, 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)
    


def main(args):
    if args.input is None: # single mode
        if args.address is None:
            raise ValueError('Need either address or path to the file')
        
        response = geocode(args.address)
        if len(response['features']) == 0:
            raise ValueError("Didn't find anything")

        print('{}, {}'.format(*pull_coords(response)))
            
    else: # batch mode 
        print('batch mode!\n')

        input_ = args.input
        output = args.output or _name(input_)
        col = args.col
        
        with open(input_, mode='r') as f:
            data = [row for row in DictReader(f)]
            
        result = _batch_geocode(data, column=col)
        
        # store
        store_csv(result, output)
        


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--address', help='specific address')
    parser.add_argument('--input', help='csv file to derive addresses from')
    parser.add_argument('--output', help='where to store result')
    parser.add_argument('--col', help='column with addresses', default='address')

    args=parser.parse_args()
    
    main(args)
    