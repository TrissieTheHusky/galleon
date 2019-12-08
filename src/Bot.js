require("dotenv").config();
const discord = require("discord.js");
const fs = require("fs");
const mongoose = require("mongoose");
const config = require("../config/master.json");
const path = require("path");
const client = new discord.Client();
client.commands = new discord.Collection();
client.config = config;
client.config.permissions = require("../config/permissions.json");

fs.readdir(path.join(__dirname, "./commands/"), (err, files) => {
  if (err) return console.error(err);
  console.log("--------");
  files.forEach(file => {
    if (!file.endsWith(".js")) return console.log(`- ${file} is not a JavaScript file, ignored.`);
    if (file.endsWith(".disabled.js")) return console.log(`? ${file.split(".")[0]} is disabled, ignored.`)

    const command = require(`./commands/${file}`);
    client.commands.set(command.meta.name, command);
    console.log(`* ${command.meta.name}`);
  });
  console.log("--------");
});

fs.readdir(path.join(__dirname, "./events/"), (err, files) => {
  if (err) return console.error(err);
  files.forEach(file => {
    if (!file.endsWith(".js")) return console.log(`- ${file} is not a JavaScript file, ignored.`);
    if (file.endsWith(".disabled.js")) return console.log(`? ${file.split(".")[0]} is disabled, ignored.`)

    const event = require(`./events/${file}`);
    let eventName = file.toLowerCase().split(".")[0];
    client.on(eventName, event.bind(null, client));
  });
});

mongoose
  .connect(process.env.DB_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(() => console.log("[MONGO] Database connected."))
  .catch(err => console.error("[MONGO] Database error:", err));

client.on("ready", () => {
  client.user.setActivity(config.status.message, { type: config.status.type });
  console.log(`[D.JS] Logged in as ${client.user.tag}`);
});

process.on("unhandledRejection", err => console.log(`---------\nUNHANDLED REJECTION: ${err.stack}\n---------`));
process.on("uncaughtException", err => console.log(`---------\nUNHANDLED EXCEPTION: ${err.stack}\n---------`));

client.login(process.env.BOT_TOKEN);
