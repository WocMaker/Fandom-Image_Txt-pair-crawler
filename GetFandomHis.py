import requests
import re
from bs4 import BeautifulSoup

Fandom_Path_Text='C:\zl\Workplace\DND corpus\Fandom_Bio'

class FandomCrawler(object):
    def __init__(self):

        self.initial_target = 'https://forgottenrealms.fandom.com/wiki/Category:Inhabitants?from=A'
        self.wiki_urls=[]
        self.url_count=1
        self.fail_count = 1
        self.pic_cont=1
        self.curr_url=1
        self.GetAll_URL(self.initial_target)
        self.curr_list=self.initial_target
        while 'from=Zeus%0AZeus' not in self.curr_list:
            try:
                self.curr_list = self.Get_next_list(self.curr_list)
            except:
                break
            self.GetAll_URL(self.curr_list)
            print("Current collected Number" + str(self.url_count))
        print("Finish collecting !!!ALL!! Urls. Total Number"+str(self.url_count))
        for One_wiki in self.wiki_urls:
            try:
                self.Download_Image_and_Txt(One_wiki)
            except:
                self.fail_count+=1
                print('This one no History')
            print("current_processing wiki Num: "+str(self.curr_url ))
            self.curr_url+=1
        print("Process !!!ALL!!! finished.")
        print("Total successful number"+str(self.pic_cont))



    def GetAll_URL(self,target):
        Prefix_url = 'https://forgottenrealms.fandom.com'
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        Li_Tag = bf.find_all('li', class_='category-page__member')
        for a_tag in Li_Tag:
            tar_str_a_tag = re.search('ref="/wiki/.*" title', str(a_tag.a))
            partical_url = tar_str_a_tag.group(0).replace('ref="', "").replace('" title', "")
            whole_url = Prefix_url + partical_url
            self.wiki_urls.append(whole_url)
            self.url_count+=1
        print(self.wiki_urls)
    def Get_next_list(self, cur_list):
        #Get next url
        target = cur_list
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        texts = bf.find_all('div', class_='category-page__pagination')
        tar_str = re.search('pagination-next wds-button wds-is-secondary" href=".*"', str(texts))
        nextpage_url = tar_str.group(0).replace('pagination-next wds-button wds-is-secondary" href="', "").replace('"', "")
        return(nextpage_url)

    def Download_Image_and_Txt(self, This_wiki_page):
        # Get Image URL
        target = This_wiki_page
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        target_name=target.split('/')[-1]
        print(target_name)
        # Get Description
        Des_Tag = bf.find_all('div', class_='mw-parser-output')
        for one_Des_Tag in Des_Tag:
            # print(one_Des_Tag)
            # Delete lables
            Txt_Des_res=str(one_Des_Tag)
            Txt_Des_res = re.sub(r'<.*?>', "", Txt_Des_res)
            # Delete Reference
            Txt_Des_res = re.sub(r'\[.*?\]', "", Txt_Des_res)
            Txt_Des_res = re.sub(r'Contents\n\n.*1 .*\n2', "", Txt_Des_res, re.DOTALL)
            Txt_Des_res = re.search('Description\n.*?Appendix\n',
                                        Txt_Des_res, re.DOTALL)
            Txt_Des_res = Txt_Des_res.group(0)
            Txt_Des_res = re.sub(r'[A-Z][a-z]*?\n', "", Txt_Des_res)
            Txt_Des_res = Txt_Des_res.replace('\n',' ')

        print(Txt_Des_res)



        # Write Description
        temp_filename_full_path_Text = Fandom_Path_Text + '/' + target_name + "." + str(self.pic_cont) + '.txt'
        with open(temp_filename_full_path_Text, "w", encoding="utf-8") as f:
            f.write(Txt_Des_res)
        self.pic_cont+=1
if __name__ == '__main__':
    Crawler=FandomCrawler()

