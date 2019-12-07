const { RichEmbed } = require("discord.js");
const DJS_VERSION = require("discord.js").version;

module.exports.execute = async (client, msg, args) => {
  msg.channel.send(
    new RichEmbed()
      .setAuthor(`${client.user.username}#${client.user.discriminator}`, client.user.avatarURL)
      .addField(`Uptime`, `${(client.uptime / 60000).toFixed(2)} minutes`, true)
      .addField(`Running on`, `Node ${process.version}`, true)
      .addField(`Using`, `Discord.js v${DJS_VERSION}`, true)
      .addField(`GitHub`, `[Open URL](https://github.com/runic-tears/def-bot)`, true)
      .setFooter(`Requested by ${msg.author.username}`, msg.author.avatarURL)
      .setColor(0x3498db)
  );
};

module.exports.meta = {
  name: "about",
  aliases: ["botinfo"],
  cooldown: 5,
  description: "Shows information about the bot"
};
