import os
import argparse
import traceback
import time
from Code.Pixiv import Pixiv

parser = argparse.ArgumentParser(
    prog="Pixiv Downloader",
    description='用于下载固定UID的收藏列表',
    epilog='Phantom-sea © limited |∀` )',
)
parser.add_argument('-c', '--cookies', type=str,
                    dest="cookie", help='设置cookie', default=False)
parser.add_argument("-m", "--mode", type=str, help="模式", default="list")
args = parser.parse_args()


def get_list_new(path: str, li: list):
    current_address = path
    for parent, dirnames, filenames in os.walk(current_address):
        for dirname in dirnames:
            pass
        for filename in filenames:
            li.append("{}/{}".format(parent, filename))
    return li


def GifZipOriUrl(P: Pixiv, ID, tryID=0):
    try:
        return P.get_gif_by_PID(ID)["body"]["originalSrc"].replace(
            "i.pximg.net", P.Mirror)
    except Exception:
        print(traceback.format_exc())
        tryID += 1
        time.sleep(5)
        if tryID >= 5:
            print(f"GIF {ID}出现异常！！！")
            return ""
        return GifZipOriUrl(P, ID, tryID)


def get_GIF_list():
    l = []
    o = []
    get_list_new("./image", l)
    for i in l:
        if "_ugoira0" in i:
            o.append(i.split("/")[-1].split("_ugoira0")[0])
    return o


def GifLIst(P: Pixiv):
    l = get_GIF_list()
    if l != []:
        open("GIF_CONTROL", "w").write("GIF_CONTROL=true")
        with open(os.path.join("image", "gifs.txt"), "w") as f:
            for ID in l:
                f.write(GifZipOriUrl(P, ID) + "\n")
    else:
        open("GIF_CONTROL", "w").write("GIF_CONTROL=false")


def Run():
    import zipfile

    def Unzip(path):
        ID = path.split("/")[-1].split("_ugoira")[0]
        outPath = os.path.join("image", ID)
        if not os.path.exists(outPath):
            os.mkdir(outPath)
        f = zipfile.ZipFile(path)
        f.extractall(outPath)
        f.close()
        return ID

    IDs = []
    ls = get_list_new("./image", [])
    for i in ls:
        if i.endswith(".zip"):
            IDs.append(Unzip(i))
    print(IDs)


def main(args):
    if args.mode == "list":
        if args.cookie is False:
            print("cookie未配置!")
        P = Pixiv(PHPSESSID=args.cookie)
        GifLIst(P)
    elif args.mode == "run":
        Run()


main(args)
