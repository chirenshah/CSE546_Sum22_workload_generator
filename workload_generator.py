import sys
import requests
import os
import argparse

correct_map = {
    'test_0': 'bathtub',
    'test_1': 'tile roof',
    'test_2': 'jigsaw puzzle',
    'test_3': 'dromedary',
    'test_4': 'jellyfish',
    'test_5': 'oxygen mask',
    'test_6': 'shower curtain',
    'test_7': 'handkerchief',
    'test_8': 'slide rule',
    'test_9': 'flamingo',
    'test_10': 'face powder',
    'test_11': 'custard apple',
    'test_12': 'zebra',
    'test_13': 'hourglass',
    'test_14': 'menu',
    'test_15': 'mosquito net',
    'test_16': 'shoal',
    'test_17': 'crossword',
    'test_18': 'leatherback sea turtle',
    'test_19': 'toy store',
    'test_20': 'website',
    'test_21': 'starfish',
    'test_22': 'boa constrictor',
    'test_23': 'envelope',
    'test_24': 'safe',
    'test_25': 'stupa',
    'test_26': 'shower curtain',
    'test_27': 'shoal',
    'test_28': 'chimpanzee',
    'test_29': 'shower curtain',
    'test_30': 'candle',
    'test_31': 'stupa',
    'test_32': 'revolver',
    'test_33': 'obelisk',
    'test_34': 'Standard Poodle',
    'test_35': 'conch',
    'test_36': 'dust jacket',
    'test_37': 'chameleon',
    'test_38': 'mosquito net',
    'test_39': 'automated teller machine',
    'test_40': 'picket fence',
    'test_41': 'aircraft carrier',
    'test_42': 'wall clock',
    'test_43': 'jellyfish',
    'test_44': 'shower cap',
    'test_45': 'tub',
    'test_46': 'sink',
    'test_47': 'mosquito net',
    'test_48': 'fireboat',
    'test_49': 'valley',
    'test_50': 'picket fence',
    'test_51': 'jigsaw puzzle',
    'test_52': 'beer glass',
    'test_53': 'brass',
    'test_54': 'military uniform',
    'test_55': 'Band-Aid',
    'test_56': 'dragonfly',
    'test_57': 'radio telescope',
    'test_58': 'cassette',
    'test_59': 'shower curtain',
    'test_60': 'shoal',
    'test_61': 'fireboat',
    'test_62': 'medicine chest',
    'test_63': 'beaker',
    'test_64': 'nipple',
    'test_65': 'shower curtain',
    'test_66': 'lacewing',
    'test_67': 'shower curtain',
    'test_68': 'slide rule',
    'test_69': 'bubble',
    'test_70': 'seat belt',
    'test_71': 'starfish',
    'test_72': 'fireboat',
    'test_73': 'brass',
    'test_74': 'bubble',
    'test_75': 'vault',
    'test_76': 'brass',
    'test_77': 'banded gecko',
    'test_78': 'whiskey jug',
    'test_79': 'dock',
    'test_80': 'hourglass',
    'test_81': 'crossword',
    'test_82': 'spider web',
    'test_83': 'picket fence',
    'test_84': 'jeep',
    'test_85': 'carton',
    'test_86': 'cauliflower',
    'test_87': 'honeycomb',
    'test_88': 'trilobite',
    'test_89': 'magnetic compass',
    'test_90': 'hourglass',
    'test_91': 'Maltese',
    'test_92': 'mosque',
    'test_93': 'church',
    'test_94': 'ruler',
    'test_95': 'hourglass',
    'test_96': 'mosquito net',
    'test_97': 'radio telescope',
    'test_98': 'yawl',
    'test_99': 'alp',
}

parser = argparse.ArgumentParser(description='Upload images')
parser.add_argument('--num_request', type=int, help='one image per request')
parser.add_argument(
    '--url', type=str, help='URL of your backend server, e.g. http://3.86.108.221/xxxx.php')
parser.add_argument('--image_folder', type=str,
                    help='the path of the folder where images are saved on your local machine')
args = parser.parse_args()

correct_count = 0
received_count = 0
wrong_dict = {}


def send_one_request(url, image_path):
    # Define http payload, "myfile" is the key of the http payload
    global correct_count, received_count, wrong_dict
    file = {"myfile": open(image_path, 'rb')}
    r = requests.post(url, files=file)
    # Print error message if failed
    if r.status_code != 200:
        print('sendErr: '+r.url)
    else:
        image_msg = image_path.split('/')[1] + ' uploaded!'
        msg = image_msg + '\n' + 'Classification result: ' + r.text
        print(msg)


num_request = args.num_request
url = args.url
image_folder = args.image_folder
# Iterate through all the images in your local folder
for i, name in enumerate(os.listdir(image_folder)):
    if i == num_request:
        break
    image_path = image_folder + name
    send_one_request(url, image_path)
