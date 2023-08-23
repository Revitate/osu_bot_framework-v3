class AutoHostRotateLevy:
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel

        self.moved_host = False

        # Set room settings
        channel.set_mods(['FREEMOD'])
        channel.set_beatmap_checker(True)
        channel.set_ar_range((8.8, 10))
        channel.set_diff_range((0, 5.2))

        # Set commands
        channel.set_command("!skip", self.skip, "If you are host, changes the host to the next username in the queue else starts vote to skip current host")
        channel.set_command("!randmap", channel.common_commands.randmap,"When host or referee, searches for a random beatmap matching the room's limits and ranges")
        channel.set_command("!altlink", channel.common_commands.altlink,"Returns an alternate link for the current beatmap from Chimu.moe")
        channel.set_command("!topdiff", channel.common_commands.topdiff,"When host, upgrades the beatmap to the highest difficulty within the room limits and ranges")
        channel.set_command("!update", channel.common_commands.update_beatmap, "Updates current beatmap")
        channel.set_command("!fight", channel.common_commands.fight, "Fight another user! Victories stack up.")
        channel.set_command("!pp", channel.common_commands.calculate_pp, "Calculate pp for current beatmap")
        channel.set_command("R̲e̲f̲e̲r̲e̲e̲ C̲o̲m̲m̲a̲n̲d̲s̲", "")
        channel.set_command("*skip", self.skip, "Changes the host to the next username in the queue")
        channel.set_command("*implement", channel.common_commands.implement_logic_profile, "Implements a logic profile")
        channel.set_command("*logic_profiles", channel.common_commands.get_logic_profiles, "Shows available logic profiles")
        channel.set_command("*ar_range", channel.common_commands.ar_range, "Sets the ar range for the room. e.g. *ar_range 5.5 8")
        channel.set_command("*od_range", channel.common_commands.od_range, "Sets the od range for the room. e.g. *od_range 5.5 8")
        channel.set_command("*hp_range", channel.common_commands.hp_range, "Sets the hp range for the room. e.g. *hp_range 5.5 8")
        channel.set_command("*cs_range", channel.common_commands.cs_range, "Sets the cs range for the room. e.g. *cs_range 5.5 8")
        channel.set_command("*bpm_range", channel.common_commands.bpm_range, "Sets the bpm range for the room. e.g. *bpm_range 80 120")
        channel.set_command("*diff_range", channel.common_commands.diff_range, "Sets the difficulty range for the room. e.g. *diff_range 4 5.99")
        channel.set_command("*length_range", channel.common_commands.length_range, "Sets the length range for the room in seconds. e.g. *length_range 0 600")
        channel.set_command("*map_status", channel.common_commands.map_status, "Sets the allowed map statuses for the room. e.g. *map_status ranked loved")
        channel.set_command("*mods", channel.common_commands.mods, "Sets the allowed mods for the room. e.g. *mods freemod")
        channel.set_command("*scoring_type", channel.common_commands.scoring_type, "Sets the allowed scoring mode for the room. e.g. *scoring_type score")
        channel.set_command("*team_type", channel.common_commands.team_type, "Sets the allowed team mode for the room. e.g. *team_type head-to-head")
        channel.set_command("*game_mode", channel.common_commands.game_mode, "Sets the allowed game mode for the room. e.g. *game_mode osu")
        channel.set_command("*start_broadcast", channel.common_commands.add_broadcast, "Starts a broadcast in the channel. e.g. *start_broadcast 5 message sent every 5min")
        channel.set_command("*stop_broadcast", channel.common_commands.del_broadcast, "Stops a broadcast in the channel given it's ID. e.g. *stop_broadcast 0")
        channel.set_command("*welcome", channel.common_commands.welcome_message, "Sets the welcome message for the room. e.g. *welcome welcome to my osu room!")
        channel.set_command("*disable_beatmap_checker", channel.common_commands.disable_beatmap_checker, "Disables beatmap checker")
        channel.set_command("*enable_beatmap_checker", channel.common_commands.enable_beatmap_checker, "Enables beatmap checker")
        channel.set_command("*enable_convert", channel.common_commands.allow_convert, "Allows beatmap conversion")
        channel.set_command("*disable_convert", channel.common_commands.disallow_convert, "Disallows beatmap conversion")
        channel.set_command("*enable_unsubmitted", channel.common_commands.allow_unsubmitted, "Allows unsubmitted beatmaps")
        channel.set_command("*disable_unsubmitted", channel.common_commands.disallow_unsubmitted, "Disallows unsubmitted beatmaps")
        channel.set_command("*add_artist_whitelist", channel.common_commands.add_artist_whitelist, "Adds an artist to the whitelist. e.g. *add_artist_whitelist eminem")
        channel.set_command("*add_artist_blacklist", channel.common_commands.add_artist_blacklist, "Adds an artist to the blacklist. e.g. *add_artist_blacklist eminem")
        channel.set_command("*add_creator_whitelist", channel.common_commands.add_beatmap_creator_whitelist, "Adds a beatmap creator to the whitelist. e.g. *add_creator_whitelist sotarks")
        channel.set_command("*add_creator_blacklist", channel.common_commands.add_beatmap_creator_blacklist, "Adds a beatmap creator to the blacklist. e.g. *add_creator_blacklist sotarks")
        channel.set_command("*del_artist_whitelist", channel.common_commands.del_artist_whitelist, "Removes an artist from the whitelist. e.g. *del_artist_whitelist eminem")
        channel.set_command("*del_artist_blacklist", channel.common_commands.del_artist_blacklist, "Removes an artist from the blacklist. e.g. *del_artist_blacklist eminem")
        channel.set_command("*del_creator_whitelist", channel.common_commands.del_beatmap_creator_whitelist, "Removes a beatmap creator from the whitelist. e.g. *del_creator_whitelist sotarks")
        channel.set_command("*del_creator_blacklist", channel.common_commands.del_beatmap_creator_blacklist, "Removes a beatmap creator from the blacklist. e.g. *del_creator_blacklist sotarks")
        channel.set_command("*add_player_blacklist", channel.common_commands.add_player_blacklist, "adds a player to the blacklist.")
        channel.set_command("*del_player_blacklist", channel.common_commands.del_player_blacklist, "Removes a player from the blacklist.")
        channel.set_command("*enable_start_on_players_ready", channel.common_commands.enable_start_on_players_ready, "enables starting the match when all players are ready")
        channel.set_command("*disable_start_on_players_ready", channel.common_commands.disable_start_on_players_ready, "disables starting the match when all players are ready")
        channel.set_command("*autostart", channel.common_commands.set_auto_start_timer, "Automatically adds start countdown after map is selected. e.g. *autostart 120")
        channel.set_command("*enable_maintain_password", channel.common_commands.enable_maintain_password, "Enables maintaining password")
        channel.set_command("*disable_maintain_password", channel.common_commands.disable_maintain_password,"disables maintaining password")
        channel.set_command("*enable_maintain_size", channel.common_commands.enable_maintain_size, "Enables maintaining size")
        channel.set_command("*disable_maintain_size", channel.common_commands.disable_maintain_size, "Disables maintaining size")
        channel.set_command("*enable_auto_download", channel.common_commands.enable_auto_download, "Enables automatic downloading of maps for the bot administrator")
        channel.set_command("*disable_auto_download", channel.common_commands.disable_auto_download,"Disables automatic downloading of maps for the bot administrator")

    def nextHost(self):
        if self.channel.get_host():
            if self.channel.get_slot_num(self.channel.get_formatted_host()) != None:
                slotnum = self.channel.get_next_full_slot_num(self.channel.get_slot_num(self.channel.get_formatted_host()) + 1)
                self.channel.set_host(self.channel.get_formatted_slot_username(slotnum))

    def skip(self, message):
        if message["username"] == self.channel.get_formatted_host() or (message["content"] == "*skip" and self.channel.has_referee(message["username"])):
            self.nextHost()
    
    def on_join(self, username):
        if self.channel.get_users() == [username]:
            self.channel.set_host(username)
    
    def on_part(self, username):
        if self.channel.get_host() == username:
            if self.channel.has_users():
                self.nextHost()
                if self.channel.in_progress():
                    self.moved_host = True

    def on_match_finish(self):
        if not self.moved_host:
            self.nextHost()
        self.moved_host = False


    def on_beatmap_change(self, old_beatmap, new_beatmap):
        if old_beatmap != new_beatmap:
            self.channel.common_commands.altlink(None)