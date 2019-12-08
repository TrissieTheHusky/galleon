const { RichEmbed } = require("discord.js");
const fetch = require("node-fetch");

module.exports.execute = async (client, msg, args = null) => {
  let message = await msg.channel.send(`Loading...`);

  let catPicture = await fetch(`https://api.thecatapi.com/v1/images/search?size=full`, {
    headers: { "x-api-key": client.config.customApis.cat }
  }).then(r => r.json());

  message.edit(
    new RichEmbed()
      .setImage(catPicture[0].url)
      .setFooter(`Requested by ${msg.author.username}`, msg.author.avatarURL)
      .setColor(0x3498db)
  );
};

module.exports.meta = {
  name: "cat",
  cooldown: 5,
  description: "Gets a random cat pictures"
};
