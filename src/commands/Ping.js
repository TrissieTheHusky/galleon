const { performance } = require("perf_hooks");
const { RichEmbed } = require("discord.js");

module.exports.execute = async (client, msg, args) => {
  let t1 = performance.now();
  let message = await msg.channel.send(":ping_pong:");
  let t2 = performance.now();

  let rest = Math.round(t2 - t1);
  let heartbeat = client.ping;

  let embed = new RichEmbed();
  embed.setColor("#3498db");
  embed.setDescription(`:heartbeat: HEARTBEAT: **${heartbeat.toFixed(1)} ms** \n:hourglass: REST: **${rest.toFixed(1)} ms**`);

  message.edit({ embed });
};

module.exports.meta = {
  category: "Utils",
  name: "ping",
  description: "Gets latencies data.",
  aliases: ["pong"],
  guildOnly: true,
  cooldown: 5
};
