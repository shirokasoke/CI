import argparse
import time
import traceback
import os
from Lib.Network import Network
from Code.Pixiv import Pixiv

parser = argparse.ArgumentParser(
    prog="Pixiv Downloader",
    description='用于下载固定UID的收藏列表',
    epilog='Phantom-sea © limited |∀` )',
)
parser.add_argument('-c', '--cookies', type=str,
                    dest="cookie", help='设置cookie', default=False)
parser.add_argument("-t", "--tag",  type=str, help='收藏栏', default="")
parser.add_argument("-uid", "--uid", type=str, help='用户UID', default=False)
parser.add_argument("-m", "--mode", type=str, help="模式", default="favorite")

args = parser.parse_args()


def main(args):
    if not os.path.exists("image"):
        os.mkdir("image")
    print(args)
    if args.uid is False:
        print("UID未配置!")
        return None
    if args.cookie is False:
        print("cookie未配置!")
        return None
    n = Network({})
    P = Pixiv(n, PHPSESSID=args.cookie)
    F = open(os.path.join("image", "urllist.txt"), "w")

    def save(url):
        url = url.replace("i.pximg.net", P.Mirror)
        # url = url.replace("i.pximg.net", "i.pixiv.re")
        # with open(os.path.join("image", url.split("/")[-1]), "wb") as f:
        #     f.write(n.get(url, timeout=(10, 30)).content)
        F.write(url+"\n")

    def ID(id, tryid=0):
        try:
            T = P.geturls_by_pid(id)
            for i in T["body"]:
                save(i["urls"]["original"])
                print(i["urls"]["original"].split("/")[-1])

            if args.mode == "favorite":
                P.change_bookmark(id)
        except Exception:
            print(traceback.format_exc())
            time.sleep(5)
            tryid += 1
            if tryid >= 5:
                print(f"{id}出现异常！！！")
                return None
            ID(id, tryid)

    if args.mode == "favorite":
        L = P.get_bookmarks_all(args.uid, args.tag)

    elif args.mode == "subscribe":
        L = P.get_all_by_uid(int(args.uid))["body"]["illusts"]

    for i in L:
        ID(i)

    F.close()


main(args)
