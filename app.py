from GoogleImageScrapper import *
from patch import *
import os
from os import listdir
from os.path import join, isdir, isfile
from flask import Flask, render_template, send_from_directory, redirect, Response, url_for

# to install
# pip install requests
# pip install python-docx
# pip install nltk
# compiled from lara -html folder

# define LARA
os.environ["LARA"] = '/home/david/LaraProject/SVN/trunk/'
mypath = os.getenv('LARA') + '/Content'
compiled_path = os.getenv('LARA') + '/Content'
onlydir = [f for f in listdir(mypath) if isdir(join(mypath, f))]

html_path = os.environ["LARA"] + 'compiled/'
content_loc = os.environ["LARA"] + 'Content/'
corpus_suffix = '/corpus/local_config.json'
lara_builder = os.environ["LARA"] + 'Code/Python/lara_run.py '
lara_builder_creator = 'word_pages '
compiled_loc = os.environ["LARA"] + 'compiled/'
folder_sufix = '_from_abstract_htmlvocabpages'
py_ver = 'python3.10'
main_page_hyper = '_from_abstract_htmlvocabpages/_hyperlinked_text_.html'
pic_loc = html_path + 'pic'

app = Flask(__name__, template_folder=html_path)

alphaBet="'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','x','w','z','a','á','b','d','ð','e','é','f','g','h','i','í','j','k','l','m','n','o','ó','p','r','s','t','u','ú','v','x','y','ý','þ','æ','ö','ð'"

# import folder names
# location of the dir of files to open

# name of content availble right now


# create an abstract html
# x='/home/david/LaraProject/SVN/trunk/Content/mangiri/corpus/local_config.json'
# os.system('python3.9 /home/david/LaraProject/SVN/trunk/Code/Python/lara_run.py '+'word_pages '+x)


# returning a list with files in dir_path
def filesinDir(dir_path):
    try:
        files_in_dir = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        return files_in_dir


# returning a list with sub dir to dir_path
def dirinDir(dir_path):
    try:
        dir_in_dir = [f for f in listdir(dir_path) if isdir(join(dir_path, f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        return dir_in_dir


def getWords(dir_path, prefix_word):
    try:
        files_in_dir = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        word_list = []
        for file_name in files_in_dir:
            if prefix_word in file_name:
                word = file_name.split('_')[1].split('.')[0]
                word_list.append(word)
        return word_list


# routing


@app.route('/')
def home():
    return render_template('index.html', content=onlydir,
                           link_html='_from_abstract_htmlvocabpages/_hyperlinked_text_.html')


@app.route('/index/<name>', methods=['GET','POST'])
def index(name):
    flag = 0

    # compile only if its not existed in compiled folder
    for dir in dirinDir(compiled_path):
        if name in dir:
            if '_hyperlinked_text_.html' in filesinDir(compiled_path + '/' + dir):
                flag = 1
                break
        else:
            pass
    if flag == 0:
        ful_loc = content_loc + name + corpus_suffix
        os.system(py_ver + lara_builder + lara_builder_creator + ful_loc)

    return redirect(url_for('surf', story_name=name, name=name))


@app.route('/<path:story_name>/<name>')
def surf(name, story_name):
    lema = '_lemmas'

    if ".html" in name or ".css" in name or ".js" in name:
        return render_template('/' + story_name + '_from_abstract_htmlvocabpages/' + name)
    else:
        return render_template('/' + story_name + '_from_abstract_htmlvocabpages/' + '_hyperlinked_text_.html')


@app.route('/<story_name>/multimedia/<path:filename>', methods=['GET'])
def loading_file(filename, story_name):
    return send_from_directory(html_path + '/' + story_name + '_from_abstract_htmlvocabpages/' + "/multimedia/",
                               filename)


@app.route('/game1/<story_name>', methods=['GET'])
def generate_game1(story_name):
    story_dir = compiled_loc + story_name + folder_sufix
    words = getWords(story_dir, 'word_')
    # TODO find NOUNS
    return render_template('game1_template.html', alphabet=alphaBet,alphabet_full=alphaBet,words1=words)
    #return render_template('game1_template.html', alphabet=alphaBet,alphabet_full=alphaBet,words1=words[0:3],words2=words[4:7],words3=words[8:11],words4=words[12:15])


@app.route('/game1/<path:filename>', methods=['GET'])
def loading_file_pic_g1(filename):
    return send_from_directory(html_path, filename)


@app.route('/game1/index.html', methods=['GET'])
def g1_back_home():
    return redirect(url_for('home'))


@app.route('/game2/<story_name>', methods=['GET'])
def generate_game2(story_name):
    story_dir = compiled_loc + story_name + folder_sufix
    words = getWords(story_dir, 'word_')

    # TODO find NOUNS
    return render_template('game2_template.html', words1=words[:4],words2=words[4:8],words3=words[3:10],words4=words[4:11])


@app.route('/game2/<path:filename>', methods=['GET'])
def loading_file_pic_g2(filename):
    return send_from_directory(html_path, filename)


@app.route('/game2/index.html', methods=['GET'])
def g2_back_home():
    return redirect(url_for('home'))


@app.route('/game3/<story_name>', methods=['GET','POST'])
def generate_game3(story_name):
    story_dir = compiled_loc + story_name + folder_sufix
    words = getWords(story_dir, 'word_')

    # TODO find NOUNS
    return render_template('game3_template.html', alphabet=alphaBet,alphabet_full=alphaBet,words1=words)


@app.route('/game3/<path:filename>', methods=['GET'])
def loading_file_pic_g3(filename):
    return send_from_directory(html_path, filename)


@app.route('/game3/index.html', methods=['GET'])
def g3_back_home():
    return redirect(url_for('home'))




"""
@app.route('/game3/<story_name>',methods=['GET'])
def generate_game3(story_name):
    story_dir=compiled_loc + story_name+folder_sufix
    words=getWords(story_dir,'word_')
    #TODO find NOUNS
    #get_pic(words)#image scrapper
    return render_template('game3_template.html',words=words)

@app.route('/game3/<pic_name>/<path:filename>', methods=['GET'])
def loading_file_pic_g3(filename,pic_name):
    return send_from_directory(pic_loc+'/'+pic_name,filename)

"""
"""pic scrapper"""
def get_pic(words):
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = pic_loc

    # Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = words

    # Parameters
    number_of_images = 1
    headless = False
    min_resolution = (0, 0)
    max_resolution = (9999, 9999)

    # Main program
    for search_key in search_keys:
        # TODO if its already exist then skip
        image_scrapper = GoogleImageScraper(webdriver_path, image_path, search_key, number_of_images, headless,
                                            min_resolution, max_resolution)
        image_urls = image_scrapper.find_image_urls()
        image_scrapper.save_images(image_urls)

    # Release resources
    del image_scrapper


if __name__ == '__main__':
    app.run(debug=True)
