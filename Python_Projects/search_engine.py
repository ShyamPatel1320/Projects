import webbrowser
chrome_path = webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
f = open("data.txt","rt") 
for line in f.readlines():
    webbrowser.get('chrome').open_new_tab("https://www.google.com/search?q="+line)
f.close()
