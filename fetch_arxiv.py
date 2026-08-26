import xml.etree.ElementTree as ET
import httpx as hx
import pathlib as p
url = "https://export.arxiv.org/api/query?search_query=cat:cs.IR+AND+abs:%22dense+retrieval%22&start=0&max_results=25"
header={"User-Agent": "semantic-doc-search/1.0 (asad-butt@web.de)"}
data = hx.get(url,headers=header)
root=ET.fromstring(data.text)
# <link href="https://arxiv.org/pdf/cond-mat/0011267v1" rel="related" type="application/pdf" title="pdf"/>
ns={"atom":"http://www.w3.org/2005/Atom"}
entries=root.findall("atom:entry",ns)
for entry in entries:
    for link in entry.findall("atom:link",ns):
        if link.get("title")=="pdf":
            print(entry.find("atom:id",ns).text.split("/")[-1])
            with open ("documents/"+str(entry.find("atom:id",ns).text.split("/")[-1])+".pdf","wb") as f:
                response=hx.get(link.get("href"),headers=header)
                f.write(response.content)


    
    