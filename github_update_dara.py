# python

import requests, pprint, os, zipfile, shutil, glob, xml.etree.ElementTree

username = "adam@evd1.tv"
password = "J7EksJLsb;tYGVk"
base_url = "https://api.github.com/repos/adamohern/%s/releases/latest"
dara_path = "/Users/adam/Desktop/dara/mecco_dara"
dara_kits_path = dara_path + "/Kits"
dara_releases_path = "/Users/adam/Desktop/dara"

kits = [
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
    tmp_filename = os.path.join(dara_kits_path, kit + "_" + os.path.basename(url) + "_partial")
    r = requests.get(url, stream=True, auth=(username, password))
    if r.status_code == 200:
        with open(tmp_filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

    complete_filename = tmp_filename.replace("_partial", ".zip")
    os.rename(tmp_filename, complete_filename)
    return complete_filename

# # delete existing kits
for the_file in os.listdir(dara_kits_path):
    file_path = os.path.join(dara_kits_path, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

# download and extract
for kit in kits:
    result = requests.get(base_url % kit, auth=(username, password))
    data = result.json()
    print "downloading", data['zipball_url']
    zip_file_path = download_file(kit, data['zipball_url'])

    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    extracted_folder_name = zip_ref.namelist()[0]
    zip_ref.extractall(dara_kits_path)
    zip_ref.close()

    os.rename(os.path.join(dara_kits_path, extracted_folder_name), os.path.splitext(zip_file_path)[0])
    os.remove(zip_file_path)

# duplicate dara folder
temp_directory = dara_releases_path + "/tmp"
shutil.copytree(dara_path, temp_directory)

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
index_file = temp_directory + "/index.cfg"
index_xml = xml.etree.ElementTree.parse(index_file).getroot()
dara_version = index_xml.attrib["version"]

release_dirname = os.path.join(dara_releases_path, "mecco_dara_" + str(dara_version))

if os.path.isdir(release_dirname):
    shutil.rmtree(release_dirname)

os.rename(temp_directory, release_dirname)

# zip release directory
release_zipname = release_dirname + ".zip"

temp_file = dara_releases_path + "/tmp"
shutil.make_archive(temp_file, 'zip', release_dirname)

if os.path.isfile(release_zipname):
    os.unlink(release_zipname)
os.rename(temp_file + ".zip", release_zipname)

shutil.rmtree(release_dirname)
