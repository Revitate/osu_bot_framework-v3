# any code here will run on starting the framework
def startup(bot):
    bot.start()
    # Add below line
    # ---------------------------------------------
    # channel = bot.make_room(title="4* - 5.5* | qqzzy's AutoHostRotate", password="abc", size=16, beatmapID=22538, mods=["freemod"], game_mode="osu", team_type="head-to-head", scoring_type="score")
    # #channel = bot.join("#mp_93542641")
    # channel.set_diff_range((4, 5.5))
    # channel.set_allow_convert(False)
    # channel.set_allow_unsubmitted(False)
    # channel.set_autostart_timer(True, 120)
    # channel.implement_logic_profile("AutoHostRotate")
    # channel.change_beatmap(bot.chimu.fetch_random_beatmap(channel)["BeatmapId"])
    #channel.add_broadcast("You can type '!randmap' to search for a random map online! (see all commands by typing '!config')", 900)
    #channel.send_message("!randmap")
    #channel.add_beatmap_creator_blacklist("sotarks")
    #channel.set_length_range((0, 360))
    #channel.set_map_status(["ranked"])
    #channel.set_ar_range((8.9, 9.5))
    #channel.set_cs_range((3, 5))
    #print(bot.get_logic_profiles())

#     print(channel.get_invite_link())
#     print(channel.get_config_link())
#     print(channel.get_users())
    #print(bot.fetch_beatmap(22538))
