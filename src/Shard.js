require("dotenv").config();
const path = require("path");
const { ShardingManager } = require("discord.js");
const manager = new ShardingManager(path.join(__dirname, "./Bot.js"), {
  shardArgs: ["--ansi", "--color", "--trace-warnings"],
  token: process.env.BOT_TOKEN
});

manager.spawn();
manager.on("launch", shard => console.log(`[D.JS SHARD] Using shard ${shard.id}`));