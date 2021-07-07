import requests
import re
from bs4 import BeautifulSoup

Fandom_Path_Image='C:\zl\Workplace\pachong\FandomPC\Image'
Fandom_Path_Text='C:\zl\Workplace\pachong\FandomPC\Description'

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
                print('This one no image')
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

        texts = bf.find_all('div', class_='mw-parser-output')
        tar_str = re.search("1x, .* 2x", str(texts))
        image_url = tar_str.group(0).replace("1x, ", "").replace(" 2x", "")


        # Get Description
        Des_Tag = bf.find_all('div', class_='mw-parser-output')
        for one_Des_Tag in Des_Tag:
            tar_str_Des_tag = re.search('<h2><span class="mw-headline" id="Description">.*?</h2>\n<p>.*?</p>\n<h2>',
                                        str(one_Des_Tag), re.DOTALL)
            Des_res = tar_str_Des_tag.group(0).replace('</p>\n<h2>', '')
            Txt_Des_res = re.sub(r'<h2>.*?</h2>', "", Des_res)
            # Delete lables
            Txt_Des_res = re.sub(r'<.*?>', "", Txt_Des_res)
            # Delete Reference
            Txt_Des_res = re.sub(r'\[.*?\]', "", Txt_Des_res)
            # Delete extra space and the \n in the very first line
            Txt_Des_final_res = Txt_Des_res.replace('  ', ' ').replace('\n', '', 1)
        print(Txt_Des_final_res)


        # Download Image from URL
        res = requests.get(image_url)
        # Get file name
        target_split = target.split('/')
        target_name = target_split[-1]
        if 'img' in image_url:
            image_type = '.img'
        else:
            image_type = '.png'
        temp_filename_full_path_Image = Fandom_Path_Image + '/' + target_name + "." + str(self.pic_cont) + image_type


        # Write Image in file
        f = open(temp_filename_full_path_Image, 'wb')
        f.write(res.content)
        f.close()

        # Write Description
        temp_filename_full_path_Text = Fandom_Path_Text + '/' + target_name + "." + str(self.pic_cont) + '.txt'
        with open(temp_filename_full_path_Text, "w", encoding="utf-8") as f:
            f.write(Txt_Des_final_res)
        self.pic_cont+=1
if __name__ == '__main__':
    Crawler=FandomCrawler()

