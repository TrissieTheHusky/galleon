const { RichEmbed } = require("discord.js");
const randElem = require("sugar").Array.sample;

module.exports.execute = async (client, msg, args) => {
  const decision = randElem(["yes", "no"]);

  msg.channel.send(`**${msg.author.username}#${msg.author.discriminator}:** ${args.join(" ")}\n**My answer:** ${decision}`);
};

module.exports.meta = {
  name: "yesno",
  cooldown: 5,
  args: true,
  usage: "<your question>",
  description: "Answers with yes or no on your questions."
};
