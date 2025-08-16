import os
from typing import List, Set, Dict
from loguru import logger
from .base import APPBase


class UBlock(APPBase):
    def __init__(self,
                 blockList: List[str],
                 unblockList: List[str],
                 filterDict: Dict[str, str],
                 filterList: List[str],
                 filterList_var: List[str],
                 ChinaSet: Set[str],
                 fileName: str,
                 sourceRule: str):
        super().__init__(blockList, unblockList, filterDict, filterList, filterList_var, ChinaSet, fileName, sourceRule)

    def generate(self, isLite: bool = False):
        try:
            if isLite:
                logger.info("generate adblock UBlock Lite...")
                fileName = self.fileName.replace(".txt", "_lite.txt")
                blockList = getattr(self, 'blockListLite', []) or self.blockList
                # 可选：只保留国内域名
                blockList = [d for d in blockList if d.endswith('.cn')]
            else:
                logger.info("generate adblock UBlock Pro...")
                fileName = self.fileName
                blockList = self.blockList

            if os.path.exists(fileName):
                os.remove(fileName)

            # 写入头信息
            with open(fileName, 'a', encoding='utf-8') as f:
                f.write(f"! Title: {title}\n")
                f.write("! Homepage: %s\n" % self.homepage)
                f.write("! Source: %s/%s\n" % (self.source, os.path.basename(fileName)))
                f.write("! Version: %s\n" % self.version)
                f.write("! modified: %s\n" % self.time)
                f.write("! domains: %s\n" % len(blockList))
                f.write("!\n")
                for domain in blockList:
                    f.write("||%s^$all\n" % domain)  # 只加 $all，不生成响应
                    # f.write("||%s^$all,redirect=nooptext\n" % domain)

            logger.info("adblock UBlock %s: block=%d" % ('Lite' if isLite else 'Pro', len(blockList)))

        except Exception as e:
            logger.error("UBlock generate failed: %s" % e)
