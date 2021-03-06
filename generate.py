import argparse
import os

argparse = argparse.ArgumentParser()
argparse.add_argument("-d", "--dir", dest = "dir")

args = argparse.parse_args()

global folder
folder = args.dir or "."

def index(source):
    list = []
    
    for root, dirs, files in os.walk(source):
        relroot = os.path.abspath(os.path.join(source))
        dir = os.path.relpath(root, relroot)

        for file in files:
            filename = os.path.join(root, file)

            if os.path.isfile(filename):
                relative = os.path.join(os.path.relpath(root, relroot), file)      
                
                if relative.endswith(".html") and not "template.html" in relative and not "index.html" in relative:
                    list.append(relative)
                
    return list

global start_tag
global end_tag

start_tag = "<!-- CONTENT BEGIN -->"
end_tag = "<!-- CONTENT END -->"

if __name__ == "__main__":
    files = index(folder);
    
    global template
    with open("template.html") as f:
        template = f.read()
    
    for file in files:        
        with open(file) as f:
            print("Reading " + file)
            doc = f.read().replace("\t", "").replace("\n", "\n\t\t")
            
            title = file.replace(".html", "")[file.rfind(os.sep) + 1:len(file)]
            
            start = doc.find(start_tag)
            end = doc.find(end_tag) + len(end_tag)
            content = template.replace("%CONTENT%", doc[start:end]).replace("%TITLE%", title.title())
           
            print(content)
            
        with open(file, "w") as f:
            f.write(content)
                