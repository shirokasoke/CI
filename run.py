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

    def save(url):
        # url = url.replace("i.pximg.net", P.Mirror)
        # url = url.replace("i.pximg.net", "i.pixiv.re")
        with open(os.path.join("image", url.split("/")[-1]), "wb") as f:
            f.write(n.get(url, timeout=(10, 30)).content)

    def ID(id):
        try:
            T = P.geturls_by_pid(id)
            for i in T["body"]:
                save(i["urls"]["original"])
                print(i["urls"]["original"].split("/")[-1])
            P.change_bookmark(id)
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(5)
            ID(id)

    L = P.get_bookmarks_all(args.uid, args.tag)
    for i in L:
        ID(i)


main(args)
