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
      if (!guild) return msg.channel.send(`:warning: I cannot leave this guild, it appears to be an unexisting guild.`);
      guild.leave().catch(e => msg.channel.send(`:x: Something went wrong \`\`\`${e.message}\`\`\``));

      return msg.channel.send(`:white_check_mark: I left **${guild.name}** (\`${guild.id}\`)`);
    }

    default: {
      msg.channel.send(":x: You have invoked an invalid subcommand.");
      break;
    }
  }
};

module.exports.meta = {
  category: "Owner",
  name: "guild",
  description: "Manipulations with guilds",
  usage: "[list | leave <guildId>]",
  args: true,
  ownerOnly: true
};
