from selenium import webdriver
from time import sleep
from datetime import datetime
import pandas as pd
from json import dumps


def scrap_article(chrome, url, first_time):
    chrome.get(url=url)
    article = {}
    sleep(3)

    #article['timestamp'] = datetime.now()
    #article['url'] = url

    if first_time == True:
        try:
            article['division'] = chrome \
             .find_element_by_xpath('//*[@id="art-tags"]/a/span') \
             .text
            #article['author'] = chrome \
            # .find_element_by_xpath('//*[@id="art-header"]/div[3]/div[1]/span') \
            # .text
        except:
            article['division'] = chrome \
             .find_element_by_xpath('//*[@id="art-tags"]/span') \
             .text
        #    article['division'] = None
        #article['pub_date'] = chrome \
        #    .find_element_by_xpath('//*[@id="art-datetime"]') \
        #    .text

        #article['title'] = chrome.find_element_by_xpath('//*[@id="art-header"]/div[2]/h1').text
        article['highlight'] = chrome \
            .find_element_by_xpath('//*[@id="pagetype_art"]/div[4]/div[2]/section/article/section') \
            .text


        article['content'] = ""
        for section in chrome.find_elements_by_class_name('art_paragraph'):
            article['content'] += section.text

        try:
            article['media_src'] = chrome \
                .find_element_by_xpath('//*[@id="gazeta_article_image"]/div[1]/img') \
                .get_attribute("src")
            article['media_desc'] = chrome \
                .find_element_by_xpath('//*[@id="gazeta_article_image"]/div[1]/img') \
                .get_attribute("alt")
            article['media_type'] = 'image'
        except:
            article['media_desc'] = chrome \
                .find_element_by_xpath('//*[@id="vjs_video_3"]/div[9]') \
                .text
            article['media_src'] = chrome \
                .find_element_by_xpath('//*[@id="vjs_video_3_html5_api"]') \
                .get_attribute("src")
            article['media_type'] = 'video'

    sleep(6)
    for i in range(20):
        if click_expand_comments(chrome):
            break
        else:
            if click_popup(chrome):
                click_expand_comments(chrome)

    sleep(1)
    for showSubcommentsButton in chrome \
            .find_element_by_xpath('//*[@id="pagetype_art"]/main/div/section/div[2]/div[2]/section/section') \
            .find_elements_by_class_name('cResShow'):
        chrome.execute_script("arguments[0].scrollIntoView();", showSubcommentsButton)
        chrome.execute_script("window.scrollBy(0, -50);")
        showSubcommentsButton.click()

    article['comments'] = get_comments(chrome)
    return dumps(article)


def get_comments(chrome):
    allComments = []
    for mainCommentContainer in chrome \
            .find_element_by_xpath('//*[@id="pagetype_art"]/main/div/section/div[2]/div[2]/section/section') \
            .find_elements_by_class_name('cResHidden'):
        cContainer = {
            'main_comment': {},
            'sub_comments': []
        }

        cContainer['main_comment']['id'] = mainCommentContainer \
            .get_attribute("itemid") \
            .split(':')[-1]
        cContainer['main_comment']['author'] = mainCommentContainer \
            .find_elements_by_class_name('cName')[0] \
            .text
        cContainer['main_comment']['date'] = mainCommentContainer \
            .find_elements_by_class_name('cDate')[0] \
            .text
        cContainer['main_comment']['body'] = mainCommentContainer \
            .find_elements_by_class_name('cBody')[0] \
            .text \
            .replace(u'\n', ' ')
        cContainer['main_comment']['upvotes'] = mainCommentContainer \
            .find_element_by_class_name('cVoteUp') \
            .text
        cContainer['main_comment']['downvotes'] = mainCommentContainer \
            .find_element_by_class_name('cVoteDown') \
            .text
        if 'flag_SUSPICIOUS' in mainCommentContainer.get_attribute("class"):
            cContainer['main_comment']['suspicious'] = True
        else:
            cContainer['main_comment']['suspicious'] = False

        for subComment in mainCommentContainer \
                .find_elements_by_class_name('cRow'):
            tmpCommentContainer = {}

            tmpCommentContainer['id'] = subComment \
                .get_attribute("itemid") \
                .split(':')[-1]
            tmpCommentContainer['author'] = subComment \
                .find_element_by_class_name('cName').text
            tmpCommentContainer['date'] = subComment \
                .find_element_by_class_name('cDate').text
            try:
                tmpCommentContainer['reply_to'] = subComment \
                    .find_element_by_class_name('cBody') \
                    .text \
                    .split('\n')[0] \
                    .replace('@', '')
                tmpCommentContainer['body'] = subComment \
                    .find_element_by_class_name('cBody') \
                    .text \
                    .split('\n')[1]
            except IndexError:
                tmpCommentContainer['body'] = subComment \
                    .find_element_by_class_name('cBody') \
                    .text
            tmpCommentContainer['upvotes'] = subComment \
                .find_element_by_class_name('cVoteUp') \
                .text
            tmpCommentContainer['downvotes'] = subComment \
                .find_element_by_class_name('cVoteDown') \
                .text
            if 'flag_SUSPICIOUS' in subComment.get_attribute("class"):
                tmpCommentContainer['suspicious'] = True
            else:
                tmpCommentContainer['suspicious'] = False

            cContainer['sub_comments'].append(tmpCommentContainer)

        allComments.append(cContainer)
    return allComments


def click_expand_comments(chrome):
    try:
        more = chrome \
            .find_element_by_xpath('//*[@id="pagetype_art"]/main/div/section/div[2]/div[2]/section/footer/div/p/a')
        chrome.execute_script("arguments[0].scrollIntoView();", more)
        chrome.execute_script("window.scrollBy(0, -50);")
        more.click()
        return True
    except:
        sleep(1)
        return False


def click_popup(chrome):
    try:
        chrome \
            .find_element_by_xpath('//*[@id="closeDDBox"]') \
            .click()
        return True
    except:
        return False


if __name__ == '__main__':
    from sys import argv
    url =  argv[1]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--executable_path=/usr/bin/chromedriver')
    chrome = webdriver.Chrome(options=chrome_options)
    #chrome = webdriver.Chrome()
    article = scrap_article(chrome, url, True)
    print(article)
    #try:
    #    df = pd.read_csv('./'+url.split('/')[-1])
    #    pd.concat([df, pd.DataFrame({"data": str(article)}, index=[len(df)])], sort=False).to_csv('./'+url.split('/')[-1])
    #except:
    #    pd.DataFrame({'data': str(article)}, index=[0]).to_csv('./'+url.split('/')[-1])

    chrome.close()
