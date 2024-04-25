# Dekomori
A Discord Bot that guards servers against spambots, scammers and such by implementing baits in onboarding. Dekomori is fully customizable so that you can choose how aggressive you want it to be against suspicious accounts. 

![Dekomori Showcase](/.github/IMAGES/showcase.png)

## 🔨 Features
- Checks for suspicious accounts based on onboarding questions.
- Completely customizable - you can toggle every single feature on and off.
- Handles most exceptions in users such as users who join repeatedly, users who join and leave, users who join and don't answer the questions, etc.
- Logs everything in a channel of your choice.
- Has a few fun commands to play around with.

## ⚙️ Installation and Usage
Dekomori is written in Python and uses discord.py. You can run it on your own machine or on a server, or you can use Docker to get it running in a few commands. If you know any other easy installation method such as docker compose, please let me know so I can add it here.
### 🐳 Docker
You can get Dekomori running easily with a few commands. Just make sure you have docker and git installed in your system.
1. Clone the repository with `git clone https://github.com/soreikomori/dekomori`.
2. Navigate to the directory with `cd dekomori`.
3. Populate the `config.toml` file with your bot token first and foremost. You can get a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
4. Customize your Dockerfile however you wish. There is a sample Dockerfile "Dockerfile.example" in the repository that you can simply run if you want, just make sure to remove the `.example` extension.
5. Build the container with `sudo docker build -t dekomori .`. 
6. Run `docker run -d --name dekomori -v ./config:/app/config dekomori`.
7. That's it! Dekomori should be running now. You can get an invite link from your Discord Developer Portal.
   
## ❓ Support
If you need help or want extra information about Dekomori, feel free to join the [support server](https://discord.gg/XwGnS3SwWZ)! I'll be happy to help you out.

## 🛠️ Contributing
If you want to contribute to Dekomori, feel free to submit a feature request issue, or fork the repository and submit a pull request. I'll review it as soon as I can. You could also join the support server above and talk to me directly.

## ❤️ Donations
Dekomori will always be fully free and open source, and there will never be any features locked behind paywalls. However, if you want to support me and my projects, you can donate to my [Ko-fi](https://ko-fi.com/soreikomori). I appreciate every donation, no matter the amount!

## 📜 License
Dekomori is licensed under the CC BY-NC-SA 4.0 license. You can read the full license [here](./LICENSE).

## 🫂 Acknowledgements
Dekomori uses [discord.py](https://github.com/Rapptz/discord.py).
Dekomori's ToS and Privacy Policy were inspired by Eresh bot's. You can find their discord server [here](https://discord.gg/yz9EtDMgX9).