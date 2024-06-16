class OsuDirect:
    def __init__(self, bot):
        self.bot = bot
        
    # beatmapset download link
    def fetch_set_download_link(self, beatmapsetID):
            return "https://api.osu.direct/d/" + str(beatmapsetID)
