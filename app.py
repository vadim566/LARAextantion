#from GoogleImageScrapper import *
import random

from GoogleImageScrapper import GoogleImageScraper
from patch import *
import os
from os import listdir
from os.path import join, isdir, isfile
from flask import Flask, render_template, send_from_directory, redirect, Response, url_for
import SVN.trunk.Code.Python.lara_utils as lara_utils
import subprocess

# to install
# pip install requests
# pip install python-docx
# pip install nltk
# compiled from lara -html folder

# define LARA
LARA= './SVN/trunk/'
mypath = LARA + 'Content'
compiled_path = LARA + 'Content'
onlydir = [f for f in listdir(mypath) if isdir(join(mypath, f))]

html_path = './SVN/trunk/compiled/'
content_loc = './SVN/trunk/Content/'
corpus_suffix = '/corpus/local_config.json'
lara_builder = LARA + 'Code/Python/lara_run.py '
lara_builder_creator = 'word_pages '
compiled_loc = LARA + 'compiled/'
folder_sufix = 'vocabpages'
index_folder_sufix='vocabpages'
multimedia_folder= "/multimedia/"
py_ver = 'python '
py_ver_w='python'
main_page_hyper = '_from_abstract_htmlvocabpages/_hyperlinked_text_.html'
hyper_page_html='vocabpages/_hyperlinked_text_.html'
pic_loc = html_path + 'pic'
slash='./'
slash_clean='/'

app = Flask(__name__, template_folder=html_path)
"""TODO extarct from meta data JASON the right language"""
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
                           link_html=main_page_hyper)


@app.route('/index/<name>', methods=['GET','POST'])
def index(name):
    flag = 0

    # compile only if its not existed in compiled folder
    for dir in dirinDir(content_loc):
        if name in dir:
            if '_hyperlinked_text_.html' in filesinDir(content_loc + slash + dir):
                flag = 1
                break
        else:
            pass
    if flag == 0:
        ful_loc = content_loc + name + corpus_suffix
      #  try:
        os.system("python "+ lara_builder + lara_builder_creator + ful_loc)
      #  except:
      #  subprocess.call(py_ver+ lara_builder + lara_builder_creator + ful_loc)
        #finally:
        return redirect(url_for('surf', story_name=name, name=name))


@app.route('/<path:story_name>/<name>')
def surf(name, story_name):
    lema = '_lemmas'

    if ".html" in name or ".css" in name or ".js" in name:
        return render_template(slash+ story_name + index_folder_sufix+slash + name)
    else:
        return render_template(slash + story_name + hyper_page_html)


@app.route('/<story_name>/multimedia/<path:filename>', methods=['GET'])
def loading_file(filename, story_name):
    return send_from_directory(html_path + slash + story_name + index_folder_sufix + multimedia_folder+slash,filename)


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

"""GAME 3"""

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


"""IMAGE SCRAPER"""

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
'''def get_pic(words):
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
'''
"""GAME 4"""

@app.route('/game4/<story_name>', methods=['GET'])
def generate_game4(story_name, file=None):
    #TODO add template game 4
    #TODO add redirecter to game4
    #TODO print build dic from metadata file
    #TODO get the metadata folder, random of all of these that inside the folder


    metaDataAudioDir=mypath+slash_clean+story_name+slash_clean+'audio'+slash_clean
    audioVersions=dirinDir(metaDataAudioDir)
    #TODO add expectaion
    File=metaDataAudioDir+audioVersions[0]+slash_clean+'metadata_help.json'
    Metadata = lara_utils.read_json_file(File)
    meta_dic=[{}]
    for m in Metadata:
        meta_dic[0].update({m['text']:m['file']})
    sentance=[]
    sounds=[]
    for key,value in meta_dic[0].items():
        sentance.append(key)
        sounds.append(value)

    """get random sentance"""
    size_of_story=len(sentance)
    rand_index=random.randint(0,size_of_story)

    """gather 4 random index for 4 wrong answers """
    rand_i=rand_index
    fake_answer=[]
    for i in range(4):

            rand_i=random.sample(range(0,size_of_story),4)



    true_match=[sentance[rand_index],sounds[rand_index]]
    bad_match=[sentance[rand_i[0]],sentance[rand_i[1]],sentance[rand_i[2]],sentance[rand_i[3]]]



    print(true_match)
    print(bad_match)


    return  render_template('game4_template.html',t_answer=true_match[0],question=true_match[1],fake_answer_0=bad_match[0],fake_answer_1=bad_match[1],fake_answer_2=bad_match[2],fake_answer_3=bad_match[3],name=story_name)
    #return render_template('game4_template.html',meta_dic=meta_dic,alphabet=alphaBet,name=story_name)


@app.route('/game4/<story_name>/<path:filename>', methods=['GET','POST'])
def loading_file_pic_g4(filename,story_name):
    metaDataAudioDir = mypath + slash_clean + story_name + slash_clean+'audio'+slash_clean
    audioVersions = dirinDir(metaDataAudioDir)
    # TODO add expectaion
   # File = metaDataAudioDir + audioVersions[0] + '/'+filename
    return send_from_directory(metaDataAudioDir+slash_clean+audioVersions[0], filename)




"""GAME 5"""

@app.route('/game5/<story_name>', methods=['GET'])
def generate_game5(story_name, file=None):
    #TODO add template game 4
    #TODO add redirecter to game4
    #TODO print build dic from metadata file
    #TODO get the metadata folder, random of all of these that inside the folder


    metaDataAudioDir=mypath+slash_clean+story_name+slash_clean+'audio'+slash_clean
    audioVersions=dirinDir(metaDataAudioDir)
    #TODO add expectaion
    File=metaDataAudioDir+audioVersions[0]+slash_clean+'metadata_help.json'
    Metadata = lara_utils.read_json_file(File)
    meta_dic=[{}]
    for m in Metadata:
        meta_dic[0].update({m['text']:m['file']})
    sentance=[]
    sounds=[]
    for key,value in meta_dic[0].items():
        sentance.append(key)
        sounds.append(value)

    """get random sentance"""
    size_of_story=len(sentance)
    rand_index=random.randint(0,size_of_story)

    """gather 4 random index for 4 wrong answers """
    rand_i=rand_index
    fake_answer=[]
    for i in range(4):

            rand_i=random.sample(range(0,size_of_story),4)



    true_match=[sentance[rand_index],sounds[rand_index]]
    bad_match=[sounds[rand_i[0]],sounds[rand_i[1]],sounds[rand_i[2]],sounds[rand_i[3]]]



    print(true_match)
    print(bad_match)


    return  render_template('game5_template.html',t_answer=true_match[1],question=true_match[0],fake_answer_0=bad_match[0],fake_answer_1=bad_match[1],fake_answer_2=bad_match[2],fake_answer_3=bad_match[3],name=story_name)



@app.route('/game5/index.html', methods=['GET'])
def g4_back_home():
    return redirect(url_for('home'))


@app.route('/game5/<story_name>/<path:filename>', methods=['GET','POST'])
def loading_file_pic_g5(filename,story_name):
    metaDataAudioDir = mypath + slash_clean + story_name + slash_clean+'audio'+slash_clean
    audioVersions = dirinDir(metaDataAudioDir)
    # TODO add expectaion
   # File = metaDataAudioDir + audioVersions[0] + '/'+filename
    return send_from_directory(metaDataAudioDir+slash_clean+audioVersions[0], filename)


@app.route('/game5/index.html', methods=['GET'])
def g5_back_home():
    return redirect(url_for('home'))




"""GAME 6"""
@app.route('/game6/<story_name>', methods=['GET'])
def generate_game6(story_name, file=None):
    #TODO add template game 4
    #TODO add redirecter to game4
    #TODO print build dic from metadata file
    #TODO get the metadata folder, random of all of these that inside the folder


    metaDataAudioDir=mypath+slash_clean+story_name+slash_clean+'audio'+slash_clean
    audioVersions=dirinDir(metaDataAudioDir)
    #TODO add expectaion
    File=metaDataAudioDir+audioVersions[0]+slash_clean+'metadata_help.json'
    Metadata = lara_utils.read_json_file(File)
    meta_dic=[{}]
    for m in Metadata:
        meta_dic[0].update({m['text']:m['file']})
    sentance=[]
    sounds=[]
    for key,value in meta_dic[0].items():
        sentance.append(key)
        sounds.append(value)

    """get random sentance"""
    size_of_story=len(sentance)
    rand_index=random.randint(0,size_of_story)





    """gather 4 random index for 4 wrong answers """
    rand_i=random.sample(range(0,size_of_story),4)



    true_match=[sentance[rand_index],sounds[rand_index]]
    bad_match=[sentance[rand_i[0]],sentance[rand_i[1]],sentance[rand_i[2]],sentance[rand_i[3]]]



    #count the words in the sentance
    words_ct=true_match[0].count(" ")
    #pick random word between word set
    rand_ct = random.sample(range(1, words_ct), 1)
    # swap the word into [-------]
    words_arr=true_match[0].split(' ')
    true_word=words_arr[rand_ct[0]]#right anwser
    words_arr[rand_ct[0]]="[--------]"
    missing_sent=" ".join(words_arr)#missing sentance to question
    #pick random words from  the wrong sentance
    bad_words=[]
    for i in range(len(bad_match)):
        bad_words_arr = bad_match[i].split(' ')
        words_ct = bad_match[i].count(" ")
        bad_rand_ct = random.sample(range(0, words_ct), 1)
        bad_words.append(bad_words_arr[bad_rand_ct[0]])#bad answer

    #send the right missing word and wrong words


    print("q:"+missing_sent)
    print("t_a:"+true_word)
    print(bad_words)


    return  render_template('game6_template.html',t_answer=true_word,question0=missing_sent,question1=true_match[1],fake_answer_0=bad_words[0],fake_answer_1=bad_words[1],fake_answer_2=bad_words[2],fake_answer_3=bad_words[3],name=story_name)


@app.route('/game6/<story_name>/<path:filename>', methods=['GET','POST'])
def loading_file_pic_g6(filename,story_name):
    metaDataAudioDir = mypath + slash_clean + story_name + slash_clean+'audio'+slash_clean
    audioVersions = dirinDir(metaDataAudioDir)
    # TODO add expectaion
   # File = metaDataAudioDir + audioVersions[0] + '/'+filename
    return send_from_directory(metaDataAudioDir+slash_clean+audioVersions[0], filename)




"""GAME 7"""
@app.route('/game7/<story_name>', methods=['GET'])
def generate_game7(story_name, file=None):
    #TODO add template game 4
    #TODO add redirecter to game4
    #TODO print build dic from metadata file
    #TODO get the metadata folder, random of all of these that inside the folder


    metaDataAudioDir=mypath+slash_clean+story_name+slash_clean+'audio'+slash_clean
    audioVersions=dirinDir(metaDataAudioDir)
    #TODO add expectaion
    File=metaDataAudioDir+audioVersions[0]+slash_clean+'metadata_help.json'
    Metadata = lara_utils.read_json_file(File)
    meta_dic=[{}]
    for m in Metadata:
        meta_dic[0].update({m['text']:m['file']})
    sentance=[]
    sounds=[]
    for key,value in meta_dic[0].items():
        sentance.append(key)
        sounds.append(value)

    """get random sentance"""
    size_of_story=len(sentance)
    rand_index=random.randint(0,size_of_story)





    """gather 4 random index for 4 wrong answers """
    rand_i=random.sample(range(0,size_of_story),4)



    true_match=[sentance[rand_index],sounds[rand_index]]
    bad_match=[sentance[rand_i[0]],sentance[rand_i[1]],sentance[rand_i[2]],sentance[rand_i[3]]]



    #count the words in the sentance
    words_ct=true_match[0].count(" ")
    #pick random word between word set
    rand_ct = random.sample(range(1, words_ct), 1)
    # swap the word into [-------]
    words_arr=true_match[0].split(' ')
    true_word=words_arr[rand_ct[0]]#right anwser
    words_arr[rand_ct[0]]="[--------]"
    missing_sent=" ".join(words_arr)#missing sentance to question
    #pick random words from  the wrong sentance
    bad_words=[]
    for i in range(len(bad_match)):
        bad_words_arr = bad_match[i].split(' ')
        words_ct = bad_match[i].count(" ")
        bad_rand_ct = random.sample(range(0, words_ct), 1)
        bad_words.append(bad_words_arr[bad_rand_ct[0]])#bad answer

    #send the right missing word and wrong words


    print("q:"+missing_sent)
    print("t_a:"+true_word)
    print(bad_words)


    return  render_template('game7_template.html',t_answer=true_word,question0=missing_sent,question1=true_match[1],fake_answer_0=bad_words[0],fake_answer_1=bad_words[1],fake_answer_2=bad_words[2],fake_answer_3=bad_words[3],name=story_name)


@app.route('/game7/<story_name>/<path:filename>', methods=['GET','POST'])
def loading_file_pic_g7(filename,story_name):
    metaDataAudioDir = mypath + slash_clean + story_name + slash_clean+'audio'+slash_clean
    audioVersions = dirinDir(metaDataAudioDir)
    # TODO add expectaion
   # File = metaDataAudioDir + audioVersions[0] + '/'+filename
    return send_from_directory(metaDataAudioDir+slash_clean+audioVersions[0], filename)








"""GAME 8"""
@app.route('/game8/<story_name>', methods=['GET'])
def generate_game8(story_name, file=None):
    #TODO add template game 4
    #TODO add redirecter to game4
    #TODO print build dic from metadata file
    #TODO get the metadata folder, random of all of these that inside the folder


    metaDataAudioDir=mypath+slash_clean+story_name+slash_clean+'audio'+slash_clean
    audioVersions=dirinDir(metaDataAudioDir)
    #TODO add expectaion
    File=metaDataAudioDir+audioVersions[0]+slash_clean+'metadata_help.json'
    Metadata = lara_utils.read_json_file(File)
    meta_dic=[{}]
    for m in Metadata:
        meta_dic[0].update({m['text']:m['file']})
    sentance=[]
    sounds=[]
    for key,value in meta_dic[0].items():
        sentance.append(key)
        sounds.append(value)

    """get random sentance"""
    size_of_story=len(sentance)
    rand_index=random.randint(0,size_of_story)





    """gather 4 random index for 4 wrong answers """
    rand_i=random.sample(range(0,size_of_story),4)



    true_match=[sentance[rand_index],sounds[rand_index]]
    bad_match=[sentance[rand_i[0]],sentance[rand_i[1]],sentance[rand_i[2]],sentance[rand_i[3]]]



    #split the sentance
    split_setance=true_match[0].split(" ",4)
    print(split_setance)
    random.shuffle(split_setance)

    return  render_template('game8_template.html',t_answer=true_match[0],question1=true_match[1],split_a0=split_setance[0],split_a1=split_setance[1],split_a2=split_setance[2],split_a3=split_setance[3],split_a4=split_setance[4],name=story_name)


@app.route('/game8/<story_name>/<path:filename>', methods=['GET','POST'])
def loading_file_pic_g8(filename,story_name):
    metaDataAudioDir = mypath + slash_clean + story_name + slash_clean+'audio'+slash_clean
    audioVersions = dirinDir(metaDataAudioDir)
    # TODO add expectaion
   # File = metaDataAudioDir + audioVersions[0] + '/'+filename
    return send_from_directory(metaDataAudioDir+slash_clean+audioVersions[0], filename)







if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
