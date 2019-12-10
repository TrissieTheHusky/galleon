const discord = require("discord.js");

module.exports = async (client, guild) => {
  console.log(`[GUILDS] Left ${guild.name} (${guild.id})`);

  // TODO: Send embed with more info to logging guild/via webhook
};
