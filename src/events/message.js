const discord = require("discord.js");
const cooldowns = new discord.Collection();

const NO_PERMS_MESSAGE = `:lock: You don't have permission to execute this command.`;
const GUILD_ONLY_MESSAGE = `This command can not be executed in DMs.`

module.exports = async (client, msg) => {
  if (!msg.content.startsWith(client.config.prefix) || msg.author.bot) return;

  const args = msg.content.slice(client.config.prefix.length).split(/ +/);
  const commandName = args.shift().toLowerCase();
  const command = client.commands.get(commandName) || client.commands.find(cmd => cmd.meta.aliases && cmd.meta.aliases.includes(commandName));
  if (!command) return;

  // Проверка, если команда предназначена только для владельца бота
  if (command.meta.ownerOnly) {
    if (msg.author.id !== client.config.ownerId) return msg.channel.send(NO_PERMS_MESSAGE);
  }

  // Проверка доступа к команде
  if (command.meta.minLevel) {
    let user = client.config.permissions.find(x => x.userId === msg.author.id);

    // Отменяем выполнение команды, если пользователя даже нет в списках групп
    if (user === undefined || typeof user === undefined)
      return msg.channel.send(NO_PERMS_MESSAGE);

    // Проверка доступов
    let tooLowLevel = `:lock: Your access level is too low, you can not execute \`${command.meta.name}\`.`;
    // Если минимальный уровень слишком высок - false
    let isAccessGranted = (user.flags & command.meta.minLevel) == command.meta.minLevel;
    if (!isAccessGranted) return msg.channel.send(tooLowLevel);
  }

  // Проверка на случай, если команда только серверная
  if (command.meta.guildOnly && msg.channel.type !== "text") return msg.reply(GUILD_ONLY_MESSAGE);

  // Проверка, если команда требует наличия аргументов
  if (command.meta.args && !args.length) {
    let reply = `:x: It looks like you've missed some required arguments.`;

    // Генерация верного использования команды
    if (command.meta.usage) {
      reply += `\n:wrench: Usage: \`${client.config.prefix}${command.meta.name} ${command.meta.usage}\``;
    }

    // Ответ
    return msg.channel.send(reply);
  }

  // Кулдауны
  if (!cooldowns.has(command.meta.name)) {
    cooldowns.set(command.meta.name, new discord.Collection());
  }

  const now = Date.now();
  const timestamps = cooldowns.get(command.meta.name);
  const cooldownAmount = (command.meta.cooldown || 3) * 1000;

  if (timestamps.has(msg.author.id)) {
    const expirationTime = timestamps.get(msg.author.id) + cooldownAmount;

    if (now < expirationTime) {
      const timeLeft = (expirationTime - now) / 1000;
      return msg.reply(`you need to wait **${timeLeft.toFixed(1)} seconds** more, to execute \`${command.meta.name}\` again.`);
    }
  }

  timestamps.set(msg.author.id, now);
  setTimeout(() => timestamps.delete(msg.author.id), cooldownAmount);

  // Если всё-таки все проверки прошли успешны, то выполняем команду
  command.execute(client, msg, args);
};
