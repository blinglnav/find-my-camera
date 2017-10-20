from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

with open('./result.tsv', 'w') as rf:
    for page in range(1, 20):
        print('page: %d' % page)
        URL = 'http://www.the35mm.com/product/list.html?cate_no=24&sort_method=3&page=%d' % page

        soup = BeautifulSoup(urlopen(URL), 'lxml')
        names = soup.find_all('p', class_='name')
        total_size = len(names)
        loop_cnt = 1
        for name in names:
            print('%d/%d' % (loop_cnt, total_size))
            test_link ='http://www.the35mm.com' + name.find('a').get('href')
            equipment_name = name.strong.a.find_all('span')[2].text.strip()
            test_soup = BeautifulSoup(urlopen(test_link), 'lxml')
            if not test_soup.find('img', attrs={'alt': '바로구매하기'}).find_parent('a', class_='displaynone'):
                rf.write('%s\t%s\tYES\n' % (equipment_name, test_link))
                img_src = 'http:' + test_soup.find('img', class_='BigImage').get('src')
                img_name = equipment_name.replace('.', '_').replace('?', '_').replace('!', '_').replace('/', '_') + '.jpg'
                urlretrieve(img_src, './yes_imgs/'+img_name)
            else:
                rf.write('%s\t%s\tNO\n' % (equipment_name, test_link))
            loop_cnt += 1
