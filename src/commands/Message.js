module.exports.execute = async (client, msg, args) => {
  const subcommand = args[0];
  const subcommandArgs = args.slice(1);

  switch (subcommand.toLowerCase()) {
    case "repeat": {
      let content = subcommandArgs.join(" ");

      return msg.channel.send(content);
    }

    case "edit": {
      const channelId = subcommandArgs[0];
      const messageId = subcommandArgs[1];
      const content = subcommandArgs.slice(2).join(" ");
      const channel = client.channels.get(channelId);

      if (!channel) return msg.channel.send(":x: Unknown channel ID.");

      return await channel.fetchMessages({ around: messageId, limit: 1 }).then(messages => {
        const fetchedMsg = messages.first();

        if (!fetchedMsg) return msg.channel.send(":x: It looks like invalid message ID was provided.");

        fetchedMsg
          .edit(content)
          .then(() => msg.channel.send(`:ok_hand: Message has been successfully edited!`))
          .catch(err => msg.channel.send(`:x: Something went wrong...\n:information_source: ${err.message}`));
      });
    }

    default: {
      msg.channel.send(":x: Subcommand is missing or you tried to use unexisting subcommand.");
      break;
    }
  }
};

module.exports.meta = {
  category: "Owner",
  name: "message",
  subcommands: ["repeat", "edit"],
  aliases: ["msg"],
  description: "Sending messages from bot's name",
  hidden: true,
  args: true,
  ownerOnly: true
};
