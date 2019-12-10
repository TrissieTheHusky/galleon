const { RichEmbed } = require("discord.js");

module.exports.execute = async (client, msg, args) => {
  let pages = ["page one", "page two"];
  let page = 1;

  const embed = new RichEmbed()
    .setColor(0x3498db)
    .setDescription(pages[page - 1])
    .setFooter(`Page ${page} of ${pages.length}`);

  msg.channel.send({ embed }).then(m => {
    m.react("◀️").then(r => {
      m.react("▶️");

      const backFilter = (reaction, user) => reaction.emoji.name === "◀️" && user.id === msg.author.id;
      const forwardFilter = (reaction, user) => reaction.emoji.name === "▶️" && user.id === msg.author.id;

      const back = m.createReactionCollector(backFilter, { time: 60000 });
      const forward = m.createReactionCollector(forwardFilter, { time: 60000 });

      back.on("collect", r => {
        m.reactions.map(reaction =>
          reaction.users.map(user => {
            if (user.id === msg.author.id) reaction.remove(user);
          })
        );

        if (page === 1) return;

        page--;
        embed.setDescription(pages[page - 1]);
        embed.setFooter(`Page ${page} of ${pages.length}`);
        m.edit({ embed });
      });

      forward.on("collect", r => {
        m.reactions.map(reaction =>
          reaction.users.map(user => {
            if (user.id === msg.author.id) reaction.remove(user);
          })
        );

        if (page === pages.length) return;

        page++;
        embed.setDescription(pages[page - 1]);
        embed.setFooter(`Page ${page} of ${pages.length}`);
        m.edit({ embed });
      });

      back.on("end", () => m.clearReactions());
    });
  });
};

module.exports.meta = {
  category: "Help",
  name: "pages",
  description: "test",
  cooldown: 1,
  hidden: true,
  ownerOnly: true
};
