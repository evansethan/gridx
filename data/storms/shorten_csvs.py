import csv

def newfile(path):

    lst = []
    fullpath = "data/storms/" + path

    with open(fullpath, "r") as f:

        for row in csv.DictReader(f):
            dic = {}
            if row["DAMAGE_PROPERTY"] == '' or row["DAMAGE_PROPERTY"] == '0.00K':
                continue
            elif row["DAMAGE_CROPS"] == '' or row["DAMAGE_CROPS"] == '0.00K':
                continue

            state = ' '.join(word.capitalize() for word in row["STATE"].split()) # normalize state name
            dic["year"] = row["YEAR"]
            dic["state"] = state
            dic["property_damage"] = row["DAMAGE_PROPERTY"] # only include property damage
            dic["crop_damage"] = row["DAMAGE_CROPS"]

            lst.append(dic)

    with open(f"data/storms/storms_{path}", "w") as f:

        fieldnames = lst[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lst)

def main():

    for i in range(2014,2025):
        newfile(f"{i}.csv")

if __name__ == "__main__":
    main()