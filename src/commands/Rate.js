const { RichEmbed } = require("discord.js");

module.exports.execute = async (client, msg, args) => {
  args = args.join(" ");
  if (!args.length)
    return msg.channel.send(
      `What am I supposed to rate? :thinking:\n` +
        `:wrench: Usage: \`${client.config.prefix}${module.exports.meta.name} ${module.exports.meta.usage}\``
    );

  let givenRating = Math.floor(Math.random() * 10) + 1;
  msg.channel.send(`I would give \`${args}\` a rating of **${givenRating} / 10** stars.`);
};

module.exports.meta = {
  category: "Fun",
  name: "rate",
  cooldown: 1,
  usage: "<your text>",
  description: "Rates things you'd like to rate."
};
