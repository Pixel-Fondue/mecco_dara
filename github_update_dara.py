# python

import sys, traceback
import requests, pprint, os, zipfile, shutil, glob, xml.etree.ElementTree, getpass
import json
from os.path import expanduser
#from git import Repo

BASE_URL = "https://api.github.com/repos/adamohern/%s/releases/latest"
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
print "base path:", BASE_PATH

config_file_path = os.path.join(BASE_PATH, "_github_credentials")
print "config file path:", config_file_path

KIT_NAME = "mecco_dara"
DARA_PATH = os.path.join(BASE_PATH, KIT_NAME)
print "dara path:", DARA_PATH

DARA_KITS_PATH = os.path.join(DARA_PATH, "Kits")
print "dara kits path:", DARA_KITS_PATH

DARA_WIP_PATH = os.path.join(BASE_PATH, "wip")
print "dara WIP path:", DARA_WIP_PATH

DARA_RELEASES_PATH = os.path.join(BASE_PATH, "releases")
print "dara releases path:", DARA_RELEASES_PATH


KITS = [
    'mecco_neatFreak',
    'mecco_solo',
    'mecco_tabbyCat',
    'mecco_bling',
    'mecco_cropper',
    'mc_noodles',
    'mc_lifesaver',
    'mecco_flipper',
    'mecco_ignition',
    'mecco_kelvin',
    'mecco_metermade',
    'mecco_passify',
    'mecco_renderMonkey',
    'mecco_replay',
    'mecco_snap',
    'mecco_tagger',
    'mecco_wheely',
    'mecco_Zen'
]

def set_github_credentials():
    global USERNAME
    global PASSWORD

    try:
        config_file = open(config_file_path)
        config = json.load(config_file)
        USERNAME = config['GITHUB_USERNAME']
        PASSWORD = config['GITHUB_PASSWORD']
    except:
        print "Username:"
        USERNAME = raw_input()
        if 'PYCHARM' in os.environ:
            PASSWORD = raw_input()
        else:
            PASSWORD = getpass.getpass('Password: ')

        config = {'GITHUB_USERNAME':USERNAME, 'GITHUB_PASSWORD':PASSWORD}
        config_file = open(config_file_path, 'w')
        json.dump(config, config_file)

    finally:
        print "username:", USERNAME
        print "password:", PASSWORD[0] + "..."

def download_file(kit, url):
    tmp_filename = os.path.join(DARA_KITS_PATH, kit + "_" + os.path.basename(url) + "_partial")
    r = requests.get(url, stream=True, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        with open(tmp_filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

    complete_filename = tmp_filename.replace("_partial", ".zip")
    if os.path.exists(complete_filename):
        os.remove(complete_filename)
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

def make_dirs():
    # create Kits foler if it doesn't exist:
    if not os.path.exists(DARA_KITS_PATH):
        os.makedirs(DARA_KITS_PATH)

    # create releases foler if it doesn't exist:
    if not os.path.exists(DARA_RELEASES_PATH):
        os.makedirs(DARA_RELEASES_PATH)

# download and extract
def download_releases():
    for kit in KITS:
        try:
            rest_api_response = requests.get(BASE_URL % kit, auth=(USERNAME, PASSWORD))
            rest_api_response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print err
            sys.exit(1)
        data = rest_api_response.json()

        target_path = os.path.join(DARA_KITS_PATH, kit)
        target_cfg = os.path.join(target_path, "index.cfg")
        if os.path.exists(target_cfg) and os.path.isfile(target_cfg):
            repo_version = data['tag_name']
            config_xml = xml.etree.ElementTree.parse(target_cfg).getroot()
            local_version = config_xml.attrib["version"]
            if local_version == repo_version:
                print "up to date %s..." % data['zipball_url']
                continue

        if os.path.exists(target_path):
            shutil.rmtree(target_path)

        print "downloading %s..." % data['zipball_url']

        zip_file_path = download_file(kit, data['zipball_url'])
        extracted_folder_name = extract_zip_file(zip_file_path, DARA_KITS_PATH)

        extracted_folder_name = os.path.join(DARA_KITS_PATH, extracted_folder_name)

        # retrieve actual kit name (just in case it's not the same as the github repo name)
        index_file = os.path.join(extracted_folder_name, "index.cfg")
        index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        real_kit_name = index_xml.attrib["kit"]

        os.rename(extracted_folder_name, target_path)
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
        if '.gitattributes' in files:
            os.unlink(os.path.join(temp_directory, directory, '.gitattributes'))
        if '.git' in subdirs:
            shutil.rmtree(os.path.join(temp_directory, directory, '.git'))
        for pyc_file in [f for f in files if f.lower().endswith('.pyc')]:
            try:
                os.unlink(pyc_file)
            except:
                print traceback.print_exc()

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

# update/clone wip
def update_wip():
    try:
        os.mkdir(DARA_WIP_PATH)
    except:
        pass

    for kit in KITS:
        try:
            repo_url = 'https://%s:%s@github.com/adamohern/%s' % (USERNAME, PASSWORD, kit)
            dest_path = os.path.join(DARA_WIP_PATH, kit)
            if os.path.exists(dest_path):
                print 'Update', kit
#                repo = Repo(dest_path)
#                origin = repo.remotes.origin
#                origin.pull(rebase=True)
#                origin.push()
                os.chdir(dest_path)
                os.system("git pull --rebase")
                os.system("git push")
            else:
                print "Cloning", kit
                #Repo.clone_from(repo_url, os.path.join(DARA_WIP_PATH, kit))
                os.system("git clone {0} {1}".format(repo_url, dest_path))

        except requests.exceptions.HTTPError as err:
            print err
            sys.exit(1)
        continue
        data = rest_api_response.json()

        target_path = os.path.join(DARA_KITS_PATH, kit)
        target_cfg = os.path.join(target_path, "index.cfg")
        if os.path.exists(target_cfg) and os.path.isfile(target_cfg):
            repo_version = data['tag_name']
            config_xml = xml.etree.ElementTree.parse(target_cfg).getroot()
            local_version = config_xml.attrib["version"]
            if local_version == repo_version:
                print "up to date %s..." % data['zipball_url']
                continue

        if os.path.exists(target_path):
            shutil.rmtree(target_path)

        print "downloading %s..." % data['zipball_url']

        zip_file_path = download_file(kit, data['zipball_url'])
        extracted_folder_name = extract_zip_file(zip_file_path, DARA_KITS_PATH)

        extracted_folder_name = os.path.join(DARA_KITS_PATH, extracted_folder_name)

        # retrieve actual kit name (just in case it's not the same as the github repo name)
        index_file = os.path.join(extracted_folder_name, "index.cfg")
        index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        real_kit_name = index_xml.attrib["kit"]

        os.rename(extracted_folder_name, target_path)
        os.remove(zip_file_path)

    # duplicate dara folder
    temp_directory = os.path.join(DARA_RELEASES_PATH, "tmp")
    shutil.copytree(DARA_PATH, temp_directory)

    # # delete cruft
    for directory, subdirs, files in os.walk(temp_directory):
        if '.gitignore' in files:
            os.unlink(os.path.join(temp_directory, directory, '.gitignore'))
        if '.gitmodules' in files:
            os.unlink(os.path.join(temp_directory, directory, '.gitmodules'))
        if '.gitattributes' in files:
            os.unlink(os.path.join(temp_directory, directory, '.gitattributes'))
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

if __name__ == '__main__':
    try:
        set_github_credentials()
        make_dirs()
        download_releases()
        update_wip()

    except BaseException as e:
        print traceback.print_exc()
        raise

    finally:
        raw_input('(Press <Enter> to close)')
