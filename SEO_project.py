import requests
import bs4
import re

print('''This tool for SEO is valid for any URL, for testing purposes
user can enter any of the following :
      >   http://www.niitstudent.com
      >   http://python.org
      >   https://xlsxwriter.readthedocs.io
      >   https://www.training.com
      >   https://www.india.gov.in ''')

# Use of regular expressions for checking it's validation.
pattern_url = re.compile("[http://|https://]")
url = input("\nEnter the URL of your intrest: ")

m = pattern_url.match(url)

if m :
    print("\n__Request inprocess__ ")
    try:
        res=requests.get(url)
    except Exception as e:
        print('\n',e)

    V = res.text

    soup = bs4.BeautifulSoup(V,'html.parser')
    for script in soup(['script','style']):
        script.extract()
        text = soup.get_text()

# Geting the lines form parsed data.
    lines = (line.strip() for line in text.split())

# Getting list of words form list of lines.
    lis = [ x for x in lines]
    total_words = len(lis)

# The words to be ignored from the list of words.
    ignore = ['a','be','ï»¿', 'not', 'the', 'of','to','The','you',
'cannot', 'be','&', 'is',',', '.', 'at', 'if','1','2','3','4',
',','.','>>>','#','=','-','go','<','>','?',',',':','/','{','[','}',',',']','to','all','by','and',
'are', 'in', 'on', 'that', 'of', 'your', 'for',
'above','an','where','go','be','it','its','will','these','one','where','what','with','|',
'whom','new']

# Getting the list of useful words.
    for word in list(lis):
              if word in ignore:
                  lis.remove(word)

# Finding frequency of words.
    data={}
    for word in lis:
            data[word]=data.setdefault(word, 0)+1

# For geting five highest frequency words.
    from collections import Counter
    new_data = dict(Counter(data).most_common(5))

    def getlist(new_data):
        return list(new_data.keys())

    keywords = getlist(new_data)

    frequencies = list(new_data.values())

    density = [(x/total_words)*100 for x in frequencies]

# using Excel to analyse the density data.
    import xlsxwriter

    workbook = xlsxwriter.Workbook('D:\\Density_analysis.xlsx')
    worksheet = workbook.add_worksheet()

    headings = ['S.No.','Keyword', 'Density']
    Serial = [1,2,3,4,5]
    bold = workbook.add_format({'bold': True})

    worksheet.set_column('B:C' , 15)
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', Serial)
    worksheet.write_column('B2', keywords)
    worksheet.write_column('C2', density)

# Create a new chart object.
    chart1 = workbook.add_chart({'type': 'column'})

# Add a series of data to the Chart.
    chart1.add_series({'name':'=Sheet1!$C$1',
                   'categories':'=Sheet1!$B$2:$B$6',
                   'values':'=Sheet1!$C$2:$C$6',})

# Add a chart title and some axis labels.
    chart1.set_title ({'name': 'Analysis of Density of Keywords'})
    chart1.set_x_axis({'name': 'Keywords ---------->'})
    chart1.set_y_axis({'name': 'Densities ---------->'})

# Set an Excel chart style. Colors with white outline and shadow.
    chart1.set_style(27)

# Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart('D5', chart1, {'x_offset': 25, 'y_offset': 10})

    workbook.close()

    print('''\nSccessfull analysis of URL
\nYou can open file - 'Density_analysis' in your (D:) drive ''')


    from pyexcel_xls import read_data

    data = read_data("D:\\Density_analysis.xlsx")
    print(data)

else:
    print('\n________*INVALID URL*________')

