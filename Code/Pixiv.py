from Lib.Network import Network
import re


class Pixiv():
    "https://sirin.coding.net/public/api/Pixiv/git/files/master/method.py"

    header = {
        # "Host": "www.pixiv.net",
        "referer": "https://www.pixiv.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
    }
    Mirror = "piv.sirin.top"
    Logined = False
    "登录设置"
    csrf = None

    def __init__(self, s=Network({}), PHPSESSID="") -> None:
        '''
        PHPSESSID为登录后Cookie中名为PHPSESSID的对应值\t请登录后按F12打开开发者工具寻找\n
        可以选择不登录,即保持为空,但是获取到的数据会有一定时间的延后(Pixiv官方的锅)\n
        目前找不到不登录不出现延时的API
        '''
        self.s = s
        if PHPSESSID != "":
            self.header["Cookie"] = f"PHPSESSID={PHPSESSID}"
            self.Logined = True
        self.s.changeHeader(header=self.header)

    def get(self, url, **kwargs):
        r = self.s.get(url, **kwargs)
        return r.json()

    # def dns(self):
    #     url = "https://1.1.1.1/dns-query?name=www.pixiv.net&type=A"
    #     return self.get(
    #         url, headers={"Accept": "application/dns-json"}, noDefaultHeader=True)

    def notification(self):
        url = "https://www.pixiv.net/ajax/notification"
        return self.get(url)

    def check_login_state(self) -> bool:
        "登录正常返回True"
        r = self.notification()
        return r["error"] == False

    def check_logined_state(self) -> bool:
        "登录状态匹配设置返回True"
        r = self.check_login_state()
        return r == self.Logined

    def get_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}"
        return self.get(url)

    def geturls_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}/pages"
        return self.get(url)

    def get_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/top?lang=zh"
        return self.get(url)

    def get_all_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/all?lang=zh"
        return self.get(url)

    def get_by_Nid(self, NoverID):
        url = f"https://www.pixiv.net/ajax/novel/{NoverID}?lang=zh"
        return self.get(url)

    def get_bookmarks_by_uid(self, uid, tag="", p=0, limit=48):
        "tag是分类，默认未分类"
        offset = p * limit
        url = f"https://www.pixiv.net/ajax/user/{uid}/illusts/bookmarks?tag={tag}&offset={offset}&limit={limit}&rest=show&lang=zh"
        return self.get(url)

    def get_bookmarks_all(self, uid, tag=""):
        fin = []
        p = 0
        r = self.get_bookmarks_by_uid(uid, tag)
        while len(r["body"]["works"]) != 0:
            for i in r["body"]["works"]:
                fin.append(i["id"])
            p += 1
            r = self.get_bookmarks_by_uid(uid, tag, p=p)
        print(f'收藏获取情况：{len(fin) == r["body"]["total"]}')
        return fin

    def remove_bookmark(self, bookmarkid, tag: list = ["save"]):
        url = "https://www.pixiv.net/ajax/illusts/bookmarks/remove_tags"
        r = self.s.post(url, json={"removeTags": tag,
                                   "bookmarkIds": [str(bookmarkid)]}, headers={"x-csrf-token": self.csrf}
                        ).json()
        if r["message"] == "请重新登录。如果出现的问题仍未解决，请重新启动浏览器。":
            self.get_csrf()
            self.remove_bookmark(bookmarkid, tag)
        return r["error"] == False

    def add_bookmark(self, bookmarkid, tag: list = ["saved"]):
        url = "https://www.pixiv.net/ajax/illusts/bookmarks/add_tags"
        r = self.s.post(url, json={"tags": tag,
                                   "bookmarkIds": [str(bookmarkid)]}, headers={"x-csrf-token": self.csrf}
                        ).json()
        if r["message"] == "请重新登录。如果出现的问题仍未解决，请重新启动浏览器。":
            self.get_csrf()
            self.add_bookmark(bookmarkid, tag)
        return r["error"] == False

    def change_bookmark(self, pid):
        if self.csrf == None:
            self.get_csrf()
        bookmarkid = self.get_by_pid(pid)["body"]["bookmarkData"]["id"]
        # if self.remove_bookmark(bookmarkid, ["save"]):
        #     if self.add_bookmark(bookmarkid, ["saved"]):
        #         print(f"{pid}书签更新完成")
        #         return None
        if self.add_bookmark(bookmarkid, ["saved"]):
            print(f"{pid}书签更新完成")
            return None
        print(f"{pid}书签更新异常")

    def get_csrf(self):
        if self.csrf != None:
            return self.csrf
        r = self.s.get("https://www.pixiv.net/").text
        self.csrf = re.findall(r'{\\"token\\":\\"([\s\S]+?)\\"', r)[0]
        return self.csrf

    def get_gif_by_PID(self, PID):
        url = f"https://www.pixiv.net/ajax/illust/{PID}/ugoira_meta?lang=zh"
        return self.get(url)
