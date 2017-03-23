# python

import requests, pprint, os, zipfile, shutil, glob, xml.etree.ElementTree

USERNAME = "adam@evd1.tv"
PASSWORD = "7J2bax4NbSg3YkG"
BASE_URL = "https://api.github.com/repos/adamohern/%s/releases/latest"

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
print BASE_PATH

KIT_NAME = "mecco_dara"
DARA_PATH = os.path.join(BASE_PATH, KIT_NAME)
print DARA_PATH

DARA_KITS_PATH = os.path.join(DARA_PATH, "Kits")
print DARA_KITS_PATH

DARA_RELEASES_PATH = os.path.join(BASE_PATH, "releases")
print DARA_RELEASES_PATH


KITS = [
    'mecco_neatFreak',
    'mecco_bling',
    'mecco_cropper',
    'mecco_flipper',
    'mecco_ignition',
    'mecco_kelvin',
    'mecco_metermade',
    'mecco_passify',
    'mecco_renderMonkey',
    'mecco_snap',
    'mecco_tagger',
    'mecco_wheely',
    'mecco_Zen'
]

def download_file(kit, url):
    tmp_filename = os.path.join(DARA_KITS_PATH, kit + "_" + os.path.basename(url) + "_partial")
    r = requests.get(url, stream=True, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        with open(tmp_filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

    complete_filename = tmp_filename.replace("_partial", ".zip")
    os.rename(tmp_filename, complete_filename)
    return complete_filename

def delete_dir_contents(directory):
    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def extract_zip_file(src, dest):
    zip_ref = zipfile.ZipFile(src, 'r')
    extracted_folder_name = zip_ref.namelist()[0]
    zip_ref.extractall(dest)
    zip_ref.close()
    return extracted_folder_name

# create Kits foler if it doesn't exist:
if not os.path.exists(DARA_KITS_PATH):
    os.makedirs(DARA_KITS_PATH)

# create releases foler if it doesn't exist:
if not os.path.exists(DARA_RELEASES_PATH):
    os.makedirs(DARA_RELEASES_PATH)

# delete existing kits
delete_dir_contents(DARA_KITS_PATH)

# download and extract
for kit in KITS:
    rest_api_response = requests.get(BASE_URL % kit, auth=(USERNAME, PASSWORD))
    data = rest_api_response.json()
    print "downloading %s..." % data['zipball_url']

    zip_file_path = download_file(kit, data['zipball_url'])
    extracted_folder_name = extract_zip_file(zip_file_path, DARA_KITS_PATH)

    extracted_folder_name = os.path.join(DARA_KITS_PATH, extracted_folder_name)

    # retrieve actual kit name (just in case it's not the same as the github repo name)
    index_file = os.path.join(extracted_folder_name, "index.cfg")
    index_xml = xml.etree.ElementTree.parse(index_file).getroot()
    real_kit_name = index_xml.attrib["kit"]

    os.rename(extracted_folder_name, os.path.join(DARA_KITS_PATH, real_kit_name))
    os.remove(zip_file_path)

# duplicate dara folder
temp_directory = os.path.join(DARA_RELEASES_PATH, "tmp")
shutil.copytree(DARA_PATH, temp_directory)

# # delete cruft
for directory,subdirs,files in os.walk(temp_directory):
    if '.gitignore' in files:
        os.unlink(os.path.join(temp_directory, directory, '.gitignore'))
    if '.gitmodules' in files:
        os.unlink(os.path.join(temp_directory, directory, '.gitmodules'))
    if '.git' in subdirs:
        shutil.rmtree(os.path.join(temp_directory, directory, '.git'))
    for pyc_file in [f for f in files if f.lower().endswith('.pyc')]:
        os.unlink(pyc_file)

# retrieve dara version
index_file = os.path.join(temp_directory, "index.cfg")
index_xml = xml.etree.ElementTree.parse(index_file).getroot()
dara_version = index_xml.attrib["version"]

release_dirname = os.path.join(DARA_RELEASES_PATH, KIT_NAME + "_" + str(dara_version))

if os.path.isdir(release_dirname):
    shutil.rmtree(release_dirname)

os.rename(temp_directory, release_dirname)

# zip release directory
release_zipname = release_dirname + ".zip"

temp_file = os.path.join(DARA_RELEASES_PATH, "tmp")
shutil.make_archive(temp_file, 'zip', release_dirname)

if os.path.isfile(release_zipname):
    os.unlink(release_zipname)
os.rename(temp_file + ".zip", release_zipname)

shutil.rmtree(release_dirname)
