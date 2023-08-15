import os
import shutil
import discord
import asyncio
import random

from discord.ui import View, Modal, TextInput, Button, button
from PIL import Image, ImageDraw, ImageFont
from Augmentor import Pipeline
from string import ascii_uppercase, digits

from util.EmbedUtils import EmbedUtils
from util.FileUtils import FileUtils

W, H = 350, 100
color = (90, 90, 90)

font: ImageFont = ImageFont.truetype("C:/Users/Enzo/PycharmProjects/Secure dpy/assets/fonts/quicksand.otf", size=60)


class CaptchaCode:

    def __init__(self, member: discord.Member, channel: discord.TextChannel, role: discord.Role,
                 captchaLength: int, timeout: int, noise: float):

        self.completed: bool = False

        self.member: discord.Member = member
        self.channel: discord.TextChannel = channel
        self.role: discord.Role = role
        self.message: discord.Message

        self.captchaLength: int = captchaLength
        self.timeout: int = timeout
        self.noise: float = noise

        self.captchaCode: str

        self.userFolder: str = f"modules/captcha/captchas/guild_{member.guild.id}/member_{member.id}"
        self.captchaPath: str

    def __randomCaptcha(self) -> str:

        return "".join(random.choices(ascii_uppercase + digits, k=self.captchaLength))

    def __drawText(self, draw: ImageDraw) -> None:

        bbox = draw.textbbox((0, 0), self.captchaCode, font=font)

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        draw.text(((W - w) / 2, (H - h) / 2), self.captchaCode, font=font, fill=color)

    def __drawNoise(self, draw: ImageDraw) -> None:

        for x in range(W):

            for y in range(H):

                if random.random() > self.noise:

                    draw.point((x, y), fill=color)

    def __randomLines(self, draw: ImageDraw) -> None:

        lines: int = random.randint(1, 4)

        for i in range(lines):

            width = random.randint(2, 6)

            x1 = random.randint(0, W)
            y1 = random.randint(0, H)
            x2 = random.randint(0, W)
            y2 = random.randint(0, H)

            draw.line([(x1, y1), (x2, y2)], width=width, fill=color)

    def __randomAugmentations(self, folder: str) -> None:

        magnitude: int = random.randint(8, 12)
        inverted: bool = bool(random.randint(0, 1))

        p = Pipeline(folder)
        p.random_distortion(1, 4, 4, magnitude)
        p.random_brightness(1, 0.50, 1.50)

        if inverted:

            p.invert(1)

        p.process()

    def newCaptcha(self) -> None:

        ID: str = FileUtils.randomID()

        self.captchaCode = self.__randomCaptcha()

        captchaFolder: str = f"{self.userFolder}/captcha_{ID}"
        os.makedirs(captchaFolder, exist_ok=True)

        image: Image = Image.new("RGB", (W, H), color=(255, 255, 255))
        draw: ImageDraw = ImageDraw.Draw(image)

        self.__drawText(draw)
        self.__drawNoise(draw)
        self.__randomLines(draw)

        image.save(f"{captchaFolder}/{ID}.png")

        self.__randomAugmentations(captchaFolder)

        self.captchaPath = f"{captchaFolder}/output/" + os.listdir(f"{captchaFolder}/output")[0]

    async def solve(self, code: str) -> bool:

        if code == self.captchaCode:

            self.completed = True

            try:

                await asyncio.gather(
                    self.member.add_roles(self.role),
                    self.message.delete()
                )

            finally:

                self.__removeUserDir()

            return True

        return False

    def __removeUserDir(self) -> None:

        try:

            shutil.rmtree(self.userFolder)

        except Exception:

            pass

    async def sendCaptchaMessage(self):

        self.message = await self.channel.send(
            content=self.member.mention,
            embed=captchaEmbed(self),
            file=discord.File(self.captchaPath, "captcha.png"),
            view=CaptchaView(self)
        )

    async def startTimeout(self):

        await asyncio.sleep(self.timeout)

        if not self.completed:

            try:

                await asyncio.gather(
                    self.member.kick(),
                    self.message.delete()
                )

            finally:

                self.__removeUserDir()


def captchaEmbed(captcha: CaptchaCode) -> discord.Embed:

    embed: discord.Embed = EmbedUtils.basicEmbed(
        title=f"Hello {captcha.member.name} !",
        description="> Before accessing this server, you need to pass a captcha verification !\n"
                    "> Memorize the code below and click \"Solve !\" button !\n\n"
                    "**Info:**\n"
                    "> - The code is composed of 6 characters (capital letters and digits numbers).\n"
                    f"> - You have {captcha.timeout // 60} minutes to complete it before being kicked."
    )
    embed.set_image(url="attachment://captcha.png")

    return embed


class SolveModal(Modal):

    response = TextInput(
        label="Enter your response here...",
        style=discord.TextStyle.short,
    )

    def __init__(self, captchaCode: CaptchaCode):

        self.captchaCode: CaptchaCode = captchaCode

        super().__init__(
            title="Solve !"
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:

        await interaction.response.defer()

        if not await self.captchaCode.solve(self.response.value):

            await interaction.followup.send("Incorrect response ! Retry !", ephemeral=True)


class CaptchaView(View):

    def __init__(self, captchaCode: CaptchaCode):

        self.captchaCode: CaptchaCode = captchaCode

        super().__init__(
            timeout=None
        )

    @button(label="Solve !", style=discord.ButtonStyle.blurple)
    async def _solve(self, interaction: discord.Interaction, button: Button):

        await interaction.response.send_modal(SolveModal(self.captchaCode))

    @button(label="New captcha !", style=discord.ButtonStyle.red)
    async def _new_captcha(self, interaction: discord.Interaction, button: discord.Button):

        button.disabled = True

        await interaction.response.edit_message(view=self)

        self.captchaCode.newCaptcha()

        await interaction.edit_original_response(
            embed=captchaEmbed(self.captchaCode),
            attachments=[discord.File(self.captchaCode.captchaPath, "captcha.png")]
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        return interaction.user == self.captchaCode.member
