import hashlib

def hashed(text):
    hs_lst = ["ah","rh","fu","cj","de","dc","aa","qe","cc","lp"]
    hs_num = [8,4,6,3,7,2,1,0,5,9]
    hs_dic = {
                "ah" : "xyz", 
                "rh": "edc",
                "fu": "qwe",
                "cj": "huo",
                "de": "cvb",
                "dc": "wdc",
                "aa": "kjg",
                "qe": "rty",
                "cc": "pop",
                "lp": "def"}
    
    for i in text:
        if i not in hs_num:
            return "ValueError: The passcode just contain only number from 0 to 9"
    
    chuoi = ""

    for i in range(len(text)):
        so = int(text[i])
        chuoi += hs_dic[hs_lst[hs_num[so]]]

    chuoi = hashlib.sha256(chuoi.encode('utf-8')).hexdigest()

    return chuoi