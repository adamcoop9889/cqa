
# coding: utf-8

# In[56]:


import re, requests

def get_cik(ticker):
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')    
    f = requests.get(URL.format(ticker), stream = True)
    results = CIK_RE.findall(f.text)
    return str(results[0])


# In[126]:


import urllib.request
from bs4 import BeautifulSoup
filings = ['8-K','10-K','10-Q','S-4']
def get_filings(ticker,filing):
    ticker = ticker.upper()
    cik = get_cik(ticker)
    link = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}'.format(cik,filing)
    with urllib.request.urlopen(link) as response:
        content = response.read()
    soup = BeautifulSoup(content,'lxml')
    archives =[]
    filings =[]
    temp =[]
    #Get all filing pages
    for links in soup.find_all(id='documentsbutton'):
        archives.append('https://www.sec.gov'+links.get('href'))
    #Get filing from page
    for i in range(0,len(archives)):
        link = archives[i]
        with urllib.request.urlopen(link) as response:
            content = response.read()
        soup = BeautifulSoup(content,'lxml')
        for links in soup.find_all('a',href=True):
            temp.append('https://www.sec.gov' + links.get('href'))
        filings.append(temp[9])
        d = {'ticker': ticker, 'link': filings}
        df = pd.DataFrame(data=d)
    return(df)

def get_all_filings(ticker):
    dfs = []
    filings = ['8-K','10-K','10-Q','S-4']
    for i in range(0,3):
        df = get_filings(ticker,filings[i])
        df = df.assign(filing=filings[i])
        dfs.append(df)
    new_df = pd.DataFrame(data=pd.concat(dfs))
    return new_df
            


# In[127]:


df = get_all_filings('aapl')
df.head()

