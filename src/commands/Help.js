const { RichEmbed } = require("discord.js");

module.exports.execute = async (client, msg, args) => {
  let commandsList = "";
  client.commands.map(cmd => {
    //if (!cmd.meta.ownerOnly)
    commandsList += `* ${cmd.meta.name}\n`;
  });

  msg.channel.send(new RichEmbed().setDescription(`All commands: \n` + commandsList));
};

module.exports.meta = {
  category: "Help",
  name: "help",
  description: "Shows information about any command or category",
  cooldown: 1,
  hidden: true
};
