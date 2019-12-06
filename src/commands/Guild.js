module.exports.execute = async (client, msg, args) => {
  const subcommand = args[0];
  const subcommandArgs = args.slice(1);

  switch (subcommand.toLowerCase()) {
    case "list": {
      let reply = "**Servers that I am a member of:** ```xl";

      client.guilds.forEach(guild => {
        reply += `\n${guild.name} (${guild.id})`;
      });

      reply += "```";

      return msg.channel.send(reply);
    }

    case "leave": {
      if (subcommandArgs.length < 1) return msg.channel.send(":x: Вы не указали `<guildID>`!");

      const guild = client.guilds.get(subcommandArgs[0]);
      guild.leave().then(g => console.log(`[D.JS] Left ${g} (${g.id})`));

      return msg.channel.send(`:white_check_mark: I left **${guild.name}** (\`${guild.id}\`)`)
    }

    default: {
      msg.channel.send(":x: Субкоманда не указана, либо указана неверная субкоманда.");
      break;
    }
  }
};

module.exports.meta = {
  name: "guild",
  description: "Manipulations with guilds",
  usage: "[list | leave <guildId>]",
  args: true,
  minLevel: 1,
  ownerOnly: true
};