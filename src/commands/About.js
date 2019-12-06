const Sugar = require("sugar");

module.exports.execute = async (client, msg, args) => {
  msg.channel.send(":ok_hand:")
};

module.exports.meta = {
  name: "about",
  aliases: ["botinfo"],
  cooldown: 5,
  description: "Shows information about the bot"
};
