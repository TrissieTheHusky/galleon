const { RichEmbed } = require("discord.js");

module.exports.execute = async (client, msg, args) => {
  let pages = [];
  let page = 1;

  client.commands.map(cmd => {
    if (!pages.find(cat => cmd.meta.category === cat.name)) pages.push({ name: cmd.meta.category, content: "" });
  });

  client.commands.map(cmd => {
    if (cmd.meta.hidden && msg.author.id !== client.config.ownerId) return;

    pages.map(cat => {
      if (cmd.meta.category === cat.name) {
        cat.content += `**❯ ${client.config.prefix}${cmd.meta.name}**\n`;
        cmd.meta.description && (cat.content += `${cmd.meta.description}\n`);
        cmd.meta.usage && (cat.content += `Usage: \`${client.config.prefix}${cmd.meta.name} ${cmd.meta.usage}\`\n`);

        cat.content += `\n`;
      }
    });
  });

  const embed = new RichEmbed()
    .setColor(0x3498db)
    .setDescription(pages[page - 1].content)
    .setTitle(pages[page - 1].name)
    .setFooter(`Page ${page} of ${pages.length}`);

  msg.channel.send({ embed }).then(m => {
    m.react("◀️").then(r => {
      m.react("▶️");

      const backFilter = (reaction, user) => reaction.emoji.name === "◀️" && user.id === msg.author.id;
      const forwardFilter = (reaction, user) => reaction.emoji.name === "▶️" && user.id === msg.author.id;

      const back = m.createReactionCollector(backFilter, { time: 60000 });
      const forward = m.createReactionCollector(forwardFilter, { time: 60000 });

      back.on("collect", r => {
        if (page === 1) return;

        // Deletes user's reactions
        // m.reactions.map(reaction =>
        //   reaction.users.map(user => {
        //     if (user.id === msg.author.id) reaction.remove(user);
        //   })
        // );

        page--;
        embed.setDescription(pages[page - 1].content);
        embed.setFooter(`Page ${page} of ${pages.length}`);
        embed.setTitle(pages[page - 1].name);
        m.edit({ embed });
      });

      forward.on("collect", r => {
        if (page === pages.length) return;

        // Deletes user's reactions
        // m.reactions.map(reaction =>
        //   reaction.users.map(user => {
        //     if (user.id === msg.author.id) reaction.remove(user);
        //   })
        // );

        page++;
        embed.setDescription(pages[page - 1].content);
        embed.setFooter(`Page ${page} of ${pages.length}`);
        embed.setTitle(pages[page - 1].name);
        m.edit({ embed });
      });

      back.on("end", () => m.clearReactions());
    });
  });
};

module.exports.meta = {
  category: "Help",
  name: "help",
  description: "Command that shows information about other commands",
  cooldown: 1
};
