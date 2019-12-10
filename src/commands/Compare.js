const randElem = require("sugar").Array.sample;

module.exports.execute = async (client, msg, args) => {
  if (args.includes("|", " | ")) args = args.join(" ").split(" | ");

  msg.channel.send(`I think that \`${randElem(args)}\` is better.`);
};

module.exports.meta = {
  category: "Fun",
  name: "compare",
  cooldown: 5,
  args: true,
  usage: "<first thing> | <second thing> | ...",
  description: "Compares anything \nSpacebar sensitive!"
};
