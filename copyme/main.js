const fs = require('fs');
const { Client, Intents } = require('discord.js');
const { token, prefix, filePath } = require('./config.json');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.on('messageCreate', async (message) => {
  if (!message.content.startsWith(prefix) || message.author.bot) return;

  const args = message.content.slice(prefix.length).trim().split(/ +/);
  const command = args.shift().toLowerCase();

  if (command === 'whitelistme') {
    const ip = args[0];
    try {
      // Append the IP to the notepad file
      fs.appendFileSync(filePath, ip + '\n');

      // Send a success message
      await message.reply(`Successfully whitelisted ${ip}`);
    } catch (error) {
      console.error(error);
      await message.reply('An error occurred while whitelisting the IP.');
    }
  } else if (command === 'showlist') {
    try {
      // Read the contents of the notepad file
      const ips = fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf-8') : '';

      // Send the list of IPs in a code block
      await message.reply(`\`\`\`ips\n${ips.trim()}\`\`\``);
    } catch (error) {
      console.error(error);
      await message.reply('An error occurred while fetching the list of IPs.');
    }
  }
});

client.login(token);
