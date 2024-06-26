import os
import threading
import random
import json
import time
from itertools import product

import requests

from GAME_ATTR import GAME_ATTR


class Chimu:
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://api.chimu.moe/v1/"
        self.session = requests.Session()
        self.redownload = False
        self.songs_directory = bot.get_osu_directory() + os.sep + "Songs"
        try:
            f = open("config" + os.sep + "unsubmitted.obf", "r")
            self.unsubmitted = f.readlines()
            f.close()
        except:
            self.unsubmitted = []

    # fetches a beatmapset dictionary object from chimu.moe
    def fetch_beatmapset(self, beatmapsetID):
        if beatmapsetID:
            url = self.url + "set/" + str(beatmapsetID)
            r = self.session.get(url)
            data = json.loads(r.text)
            if r.status_code == 200:
                return data

    # fetches a beatmap dictionary object from chimu.moe
    def fetch_beatmap(self, beatmapID):
        if beatmapID:
            url = self.url + "map/" + str(beatmapID)
            r = self.session.get(url)
            data = json.loads(r.text)
            if r.status_code == 200:
                return data

    def fetch_parent_set(self, beatmapID):
        beatmap = self.fetch_beatmap(beatmapID)
        if beatmap:
            return self.fetch_beatmapset(beatmap["ParentSetId"])

    # return list of beatmapsets based on query + provided attributes
    def search(self, query="", pages=5, js_attributes=None, **attributes):
        if js_attributes:
            attributes = js_attributes
        # construct urls
        start = 0
        if "offset" in attributes:
            start = round(attributes["offset"] / 100)
        urls = []
        for i in range(start, pages + start):
            url = self.url + "search?query=" + query.replace(" ", "%20")
            attributes["offset"] = i * 100
            for attribute in attributes:
                if attributes[attribute] != -1:
                    url += "&" + attribute + "=" + str(attributes[attribute])
            urls.append(url)
        data = []
        for url in urls:
            r = self.session.get(url)
            result = json.loads(r.text)
            if r.status_code == 200:
                data += result["data"]
            else:
                break
        return data

    # beatmapset download link
    def fetch_set_download_link(self, beatmapsetID, with_video=False):
        return "https://api.chimu.moe/v1/download/" + str(beatmapsetID) + "?n=" + str(int(with_video))

    # beatmap download link
    def fetch_download_link(self, beatmapID, with_video=False):
        beatmap = self.fetch_beatmap(beatmapID)
        if beatmap:
            beatmapsetID = beatmap["ParentSetId"]
            return "https://api.chimu.moe/v1/download/" + str(beatmapsetID) + "?n=" + str(int(with_video))
        
    # can only download with chimu
    # downloads a beatmapset to the path given, or in the framework directory
    # opening on completion will open it with the default program (osu) and deletes the file on import
    # starts on its own thread by default
    def download_beatmapset(self, beatmapsetID, path="", with_video=False, auto_open=False, blocking=False):
        if not blocking:
            x = threading.Thread(target=self.download_beatmapset, args=(beatmapsetID, path, with_video, auto_open, True,))
            x.setDaemon(True)
            x.start()
        else:
            try:
                if not self.redownload:
                    if self.songs_directory:
                        for item in os.listdir(self.songs_directory):
                            if str(beatmapsetID) in item:
                                self.bot.log("-- Beatmapset " + str(beatmapsetID) + " already owned, not downloading --")
                                return
                for item in os.listdir(path):
                    if str(beatmapsetID) in item and ".osz" in item:
                        self.bot.log("-- Beatmapset " + str(beatmapsetID) + " already downloaded, not downloading --")
                        return
            except:
                pass

            path = path.replace("/", os.sep).replace("\\", os.sep)
            if path and path[-1] != os.sep and path[-1] != "/":
                path = path + os.sep
            url = self.fetch_set_download_link(beatmapsetID, with_video=with_video)
            self.bot.log("-- Downloading beatmapset " + str(beatmapsetID) + " - " + "osu.ppy.sh/s/" + str(beatmapsetID) + " to /" + path + " --")
            then = time.time()
            file = requests.get(url)
            if file.status_code < 400 and 'message":"Error:' not in file.text:
                while time.time() - then <= 1:
                    pass
                f = open(path + str(beatmapsetID) + ".osz", "wb")
                f.write(file.content)
                f.close()
                self.bot.log("-- Downloaded beatmapset " + str(beatmapsetID) + " - " + "osu.ppy.sh/s/" + str(beatmapsetID) + " --")
                if auto_open:
                    # osu will delete the file when it's opened!
                    self.bot.log("-- Opened " + str(beatmapsetID) + " - " + "osu.ppy.sh/s/" + str(beatmapsetID) + " --")
                    os.system(path + str(beatmapsetID) + ".osz")
            else:
                self.bot.log("-- Failed to download beatmapset " + str(beatmapsetID) + " - " + "osu.ppy.sh/s/" + str(beatmapsetID) + " / request status code:" + str(file.status_code) + " --")

    # takes beatmap id instead of beatmap set id
    def download_beatmap(self, beatmapID, path="", with_video=False, auto_open=False, blocking=False):
        beatmap = self.fetch_beatmap(beatmapID)
        if beatmap:
            beatmapsetID = beatmap["ParentSetId"]
            self.download_beatmapset(beatmapsetID, path, with_video, auto_open, blocking)

    def fetch_random_beatmap(self, channel=None, js_attributes=None, **attributes):
        # grab attributes from channel object
        if "beatmap_whitelist" in attributes:
            if attributes["beatmap_whitelist"]:
                return self.fetch_beatmap(int(random.choice(attributes["beatmap_whitelist"])))
        if js_attributes:
            attributes = js_attributes
        query = ""
        if "query" in attributes:
            query = attributes["query"]
            del attributes["query"]
        if channel:
            offset = None
            if "offset" in attributes:
                offset = attributes["offset"]
            attributes = self.channel_to_attributes(channel)
            if offset:
                attributes["offset"] = offset

        status = None
        if "status" in attributes:
            if type(attributes["status"]) == str:
                attributes["status"] = [attributes["status"]]
            status = attributes["status"]
            if len(status) == 1:
                attributes["status"] = attributes["status"][0]
            else:
                del attributes["status"]
        beatmap_creator_whitelist = []
        beatmap_creator_blacklist = []
        artist_whitelist = []
        artist_blacklist = []
        beatmap_whitelist = []
        beatmap_blacklist = []
        if "beatmap_creator_whitelist" in attributes:
            beatmap_creator_whitelist = attributes["beatmap_creator_whitelist"]
            del attributes["beatmap_creator_whitelist"]
        if "beatmap_creator_blacklist" in attributes:
            beatmap_creator_blacklist = attributes["beatmap_creator_blacklist"]
            del attributes["beatmap_creator_blacklist"]
        if "artist_whitelist" in attributes:
            artist_whitelist = attributes["artist_whitelist"]
            del attributes["artist_whitelist"]
        if "artist_blacklist" in attributes:
            artist_blacklist = attributes["artist_blacklist"]
            del attributes["artist_blacklist"]
        if "beatmap_blacklist" in attributes:
            beatmap_blacklist = attributes["beatmap_blacklist"]
            del attributes["beatmap_blacklist"]
        if "beatmap_whitelist" in attributes:
            beatmap_whitelist = attributes["beatmap_whitelist"]
            del attributes["beatmap_whitelist"]

        # fetch beatmap set search results
        beatmapsets = []
        if channel:
            args = [[query], artist_whitelist, beatmap_creator_whitelist]
            if [] in args:
                args.remove([])
            if [""] in args:
                args.remove([""])
            queries = list(product(*args))
            if queries:
                for q in queries:
                    beatmapsets += self.search(" ".join(q).strip(), **attributes)
            else:
                beatmapsets = self.search(query, **attributes)
        else:
            beatmapsets = self.search(query, **attributes)

        # extract beatmaps
        beatmaps = []
        processed = []
        for beatmapset in beatmapsets:
            if beatmapset in processed:
                continue
            processed.append(beatmapset)
            for beatmap in beatmapset["ChildrenBeatmaps"]:

                if status and beatmapset["RankedStatus"] not in status:
                    continue
                elif "mode" in attributes and beatmap["Mode"] != attributes["mode"]:
                    continue
                elif "min_ar" in attributes and attributes["min_ar"] > beatmap["AR"]:
                    continue
                elif "max_ar" in attributes and beatmap["AR"] > attributes["max_ar"]:
                    continue
                elif "min_od" in attributes and attributes["min_od"] > beatmap["OD"]:
                    continue
                elif "max_od" in attributes and beatmap["OD"] > attributes["max_od"]:
                    continue
                elif "min_cs" in attributes and attributes["min_cs"] > beatmap["CS"]:
                    continue
                elif "max_cs" in attributes and beatmap["CS"] > attributes["max_cs"]:
                    continue
                elif "min_hp" in attributes and attributes["min_hp"] > beatmap["HP"]:
                    continue
                elif "max_hp" in attributes and beatmap["HP"] > attributes["max_hp"]:
                    continue
                elif "min_diff" in attributes and attributes["min_diff"] > beatmap["DifficultyRating"]:
                    continue
                elif "max_diff" in attributes and beatmap["DifficultyRating"] > attributes["max_diff"]:
                    continue
                elif "min_bpm" in attributes and attributes["min_bpm"] > beatmap["BPM"]:
                    continue
                elif "max_bpm" in attributes and beatmap["BPM"] > attributes["max_bpm"]:
                    continue
                elif "min_length" in attributes and attributes["min_length"] > beatmap["TotalLength"]:
                    continue
                elif "max_length" in attributes and beatmap["TotalLength"] > attributes["max_length"]:
                    continue
                elif query and query.lower() not in str(beatmap).lower():
                    continue
                elif channel:
                    if beatmap_creator_whitelist and beatmapset["Creator"].lower() not in beatmap_creator_whitelist and all([x not in beatmap["DiffName"].lower() for x in beatmap_creator_whitelist]):
                        continue
                    elif beatmap_creator_blacklist and beatmapset["Creator"].lower() in beatmap_creator_blacklist or any([x in beatmap["DiffName"].lower() for x in beatmap_creator_blacklist]):
                        continue
                    elif artist_whitelist and beatmapset["Artist"].lower() not in artist_whitelist:
                        continue
                    elif artist_blacklist and beatmapset["Artist"].lower() in artist_blacklist:
                        continue
                    elif beatmap_blacklist and str(beatmap["BeatmapId"]) in beatmap_blacklist:
                        continue
                    elif beatmap_whitelist and str(beatmap["BeatmapId"]) not in beatmap_whitelist:
                        continue

                beatmaps.append(beatmap)
        if beatmaps:
            beatmap = random.choice(beatmaps)
            while channel and (not channel.is_allow_unsubmitted() or channel.beatmap_checker_on()) and (str(beatmap["BeatmapId"]) in self.unsubmitted or not self.bot.fetch_beatmap(beatmap["BeatmapId"])):
                if str(beatmap["BeatmapId"]) not in self.unsubmitted:
                    self.bot.log("-- added beatmap to unsubmitted list --")
                    self.unsubmitted.append(beatmap["BeatmapId"])
                    f = open("config" + os.sep + "unsubmitted.obf", "a")
                    f.write(str(beatmap["BeatmapId"]) + "\n")
                    f.close()
                beatmap = random.choice(beatmaps)
            return beatmap

    def channel_to_attributes(self, channel):
        attributes = {}
        if channel.get_map_status() != ["any"]:
            attributes["status"] = [GAME_ATTR[status] for status in channel.get_map_status()]
        if channel.get_game_mode() != "any":
            attributes["mode"] = GAME_ATTR[channel.get_game_mode()]
        attributes["min_ar"] = channel.get_ar_range()[0]
        attributes["max_ar"] = channel.get_ar_range()[1]
        attributes["min_od"] = channel.get_od_range()[0]
        attributes["max_od"] = channel.get_od_range()[1]
        attributes["min_cs"] = channel.get_cs_range()[0]
        attributes["max_cs"] = channel.get_cs_range()[1]
        attributes["min_hp"] = channel.get_hp_range()[0]
        attributes["max_hp"] = channel.get_hp_range()[1]
        attributes["min_diff"] = channel.get_diff_range()[0]
        if channel.get_diff_range()[1] != -1:
            attributes["max_diff"] = channel.get_diff_range()[1]
        attributes["min_bpm"] = channel.get_bpm_range()[0]
        if channel.get_bpm_range()[1] != -1:
            attributes["max_bpm"] = channel.get_bpm_range()[1]
        attributes["min_length"] = channel.get_length_range()[0]
        if channel.get_length_range()[1] != -1:
            attributes["max_length"] = channel.get_length_range()[1]
        attributes["beatmap_creator_whitelist"] = channel.get_beatmap_creator_whitelist()
        attributes["beatmap_creator_blacklist"] = channel.get_beatmap_creator_blacklist()
        attributes["artist_whitelist"] = channel.get_artist_whitelist()
        attributes["artist_blacklist"] = channel.get_artist_blacklist()
        attributes["beatmap_blacklist"] = channel.get_beatmap_blacklist()
        attributes["beatmap_whitelist"] = channel.get_beatmap_whitelist()

        return attributes

    def set_songs_directory(self, path):
        self.songs_directory = path

    def get_songs_directory(self):
        return self.songs_directory

    def set_redownload(self, status):
        self.redownload = status

    def is_redownload(self):
        return self.redownload
