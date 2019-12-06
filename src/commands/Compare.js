const { RichEmbed } = require("discord.js");
const randElem = require("sugar").Array.sample;

module.exports.execute = async (client, msg, args) => {
  if (args.includes("|", " | ")) args = args.join(" ").split(" | ");

  const selected = randElem(args);

  msg.channel.send(new RichEmbed().setDescription(`In my not randomised opinion, \`${selected}\` is better.`).setColor(0x3498db));
};

module.exports.meta = {
  name: "compare",
  cooldown: 5,
  args: true,
  usage: "<first thing> | <second thing> | ...",
  description: "Compares anything \nSpacebar sensitive!"
};
