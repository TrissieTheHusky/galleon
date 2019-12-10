const discord = require("discord.js");

module.exports = async (client, guild) => {
  console.log(`[GUILDS] Joined ${guild.name} (${guild.id})`);

  // TODO: Copying the default config file with guild's ID into /config/guilds/guildId.json
  //       Send embed to logging guild/via webhook
};
