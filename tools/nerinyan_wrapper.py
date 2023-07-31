class Nerinyan:
    def __init__(self, bot):
        self.bot = bot
        
    # beatmapset download link
    def fetch_set_download_link(self, beatmapsetID):
            return "https://api.nerinyan.moe/d/" + str(beatmapsetID)
