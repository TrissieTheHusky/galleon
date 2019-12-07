const { RichEmbed } = require("discord.js");
const randElem = require("sugar").Array.sample;

module.exports.execute = async (client, msg, args) => {
  if (args.includes("|", " | ")) args = args.join(" ").split(" | ");

  const selected = randElem(args);

  msg.channel.send(`In my not randomised opinion, \`${selected}\` is better.`);
};

module.exports.meta = {
  name: "compare",
  cooldown: 5,
  args: true,
  usage: "<first thing> | <second thing> | ...",
  description: "Compares anything \nSpacebar sensitive!"
};
