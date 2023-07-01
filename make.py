from bs4 import BeautifulSoup
from pyfiglet import figlet_format

asci1 = figlet_format("NAME SVG ELEMENTS")
asci2 = figlet_format("RaJu~Made~This     help->README.md" , font = "digital" )
print(asci1)
print(asci2)
enyKey = input("Press Enter <-| to continue ~ ")
with open("input.svg", "r") as f:
  soup = BeautifulSoup(f, "xml")



sections = soup.find(id="sections")
sectionTypes = sections.find_all("g" , recursive=False)

for section in sectionTypes:
  sectionID = section["id"]
  print(f"renaming ... {sectionID} section ---->")
  groups = section.find_all("g", recursive=False)
  for group in groups:
    text = group.find("text")
    newTextID = f"{sectionID}-{text.string.lower()}-label"
    newPathID = f"{sectionID}-{text.string.lower()}-section"
    newGroupID = f"{sectionID}-{text.string.lower()}-group"
    #finding path or polygon element
    next_sibling = text.find_next_sibling()
    previous_sibling = text.find_previous_sibling()
    # renaming
    if next_sibling:
      next_sibling["id"] = newPathID
    elif previous_sibling:
      previous_sibling["id"] = newPathID
    else:
      print("sibling not found")
    text["id"] = newTextID
    group["id"] = newGroupID

  print("Done !")

#UnGroup sections
print("unGrouping ....")
for section in sectionTypes:
  groups = section.find_all("g", recursive=False)
  for group in groups:
    section.insert_before(group)
  section.decompose()


modified_svg_content = str(soup)

with open("output.svg", "w") as output_file:
    output_file.write(modified_svg_content)
    print("SVG file Created successfully")
print("<---->") 
