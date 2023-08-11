import asyncio
import os
import random
import discord

from discord.ui import View, Button, button, Modal, InputText
from PIL import Image, ImageDraw, ImageFont
from Augmentor import Pipeline
from string import ascii_uppercase, digits
from shutil import rmtree

from util.EmbedUtils import EmbedUtils
from util.FileUtils import FileUtils


def captchaEmbed(captcha) -> discord.Embed:

    embed: discord.Embed = EmbedUtils.basicEmbed(
        title=f"Hello {captcha.member.name} !",
        description="> Before accessing this server, you need to pass a captcha verification !\n"
                    "> Memorize the code below and click \"Solve !\" button !\n\n"
                    "**Info:**\n"
                    "> - The code is composed of 6 characters (capital letters and digits numbers).\n"
                    f"> - You have {captcha.kickTime // 60} minutes to complete it before being kicked."
    )
    embed.set_image(url="attachment://captcha.png")

    return embed


class CaptchaCode:

    def __init__(self, member: discord.Member, channel: discord.TextChannel, role: discord.Role, captchaLength: int,
                 kickTime: int, noise: float):

        # Captcha
        self.completed: bool = False

        # Options
        self.W, self.H = 350, 100
        self.color: tuple[int, int, int] = (90, 90, 90)
        self.captchaLength: int = captchaLength
        self.kickTime: int = kickTime
        self.noise: float = noise

        # Discord elements
        self.message: discord.Message
        self.member: discord.Member = member
        self.channel: discord.TextChannel = channel
        self.role: discord.Role = role

        # Paths
        self.userFolder: str = f"modules/captcha/files/guild_{member.guild.id}/member_{member.id}"
        self.captcha: str
        self.captchaPath: str

        # Augmentations
        self.inverted_colors: bool
        self.magnitude: int
        self.lines: int

    def __random_captcha(self) -> str:

        return "".join(random.choices(ascii_uppercase + digits, k=self.captchaLength))

    def __random_augmentations(self) -> None:

        self.inverted_colors: bool = bool(random.randint(0, 1))
        self.magnitude:int = random.randint(8, 14)
        self.lines: int = random.randint(2, 4)

    def __add_text(self, draw: ImageDraw, font: ImageFont) -> None:

        bbox = draw.textbbox((0, 0), self.captcha, font=font)

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        draw.text(((self.W - w) / 2, (self.H - h) / 2), self.captcha, font=font, fill=self.color)

    def __add_noise(self, draw: ImageDraw) -> None:

        for x in range(self.W):

            for y in range(self.H):

                if random.random() > self.noise:

                    draw.point((x, y), fill=self.color)

    def __add_lines(self, draw: ImageDraw) -> None:

        for i in range(self.lines):

            width = random.randint(2, 6)

            x1 = random.randint(0, self.W)
            y1 = random.randint(0, self.H)
            x2 = random.randint(0, self.W)
            y2 = random.randint(0, self.H)

            draw.line([(x1, y1), (x2, y2)], width=width, fill=self.color)

    def __add_augmentations(self, captchaFolder: str) -> None:

        p = Pipeline(captchaFolder)

        if self.inverted_colors:
            p.invert(1)

        p.random_brightness(1, 0.50, 1.50)
        p.random_distortion(1, 4, 4, self.magnitude)

        p.process()

    def remove_dir(self) -> None:

        try:

            rmtree(self.userFolder)

        except Exception:

            pass

    def new_captcha(self) -> None:

        ID = FileUtils.randomID()

        self.captcha = self.__random_captcha()
        captchaFolder = f"{self.userFolder}/captcha_{ID}"

        os.makedirs(captchaFolder, exist_ok=True)

        white = (255, 255, 255)

        image: Image = Image.new("RGB", (self.W, self.H), color=white)
        draw: ImageDraw = ImageDraw.Draw(image)
        font: ImageFont = ImageFont.truetype("C:/Users/Enzo/PycharmProjects/Secure/assets/fonts/quicksand.otf", size=60)

        self.__random_augmentations()

        self.__add_text(draw, font)
        self.__add_noise(draw)
        self.__add_lines(draw)

        image.save(f"{captchaFolder}/{ID}.png")

        self.__add_augmentations(captchaFolder)

        files = os.listdir(f"{captchaFolder}/output")

        self.captchaPath = f"{captchaFolder}/output/" + files[0]

    async def send_captcha_message(self):

        self.message = await self.channel.send(
            content=self.member.mention,
            embed=captchaEmbed(self),
            file=discord.File(self.captchaPath, "captcha.png"),
            view=CaptchaView(self, self.role)
        )

    async def start_timeout(self):

        await asyncio.sleep(self.kickTime)

        if not self.completed:

            try:

                self.remove_dir()

                await self.member.kick()
                await self.message.delete()

            except Exception:

                pass


class SolveModal(Modal):

    def __init__(self, captchaCode: CaptchaCode, role: discord.Role):

        self.captcha = captchaCode
        self.role = role

        super().__init__(
            InputText(
                label="Enter your response here...",
                style=discord.InputTextStyle.short,
                min_length=captchaCode.captchaLength,
                max_length=captchaCode.captchaLength

            ),
            title="Solve !"
        )

    async def callback(self, interaction: discord.Interaction):

        if self.children[0].value.lower() == self.captcha.captcha.lower():

            try:

                self.captcha.completed = True

                await interaction.response.defer()

                await interaction.user.add_roles(self.role)
                await interaction.message.delete()

            finally:

                self.captcha.remove_dir()

        else:

            await interaction.response.send_message("Incorrect response ! Retry !", ephemeral=True)


class CaptchaView(View):

    def __init__(self, captchaCode: CaptchaCode, role: discord.Role):

        self.captcha = captchaCode
        self.role: discord.Role = role

        super().__init__(
            timeout=600,
            disable_on_timeout=True
        )

    @button(label="Solve !", style=discord.ButtonStyle.blurple)
    async def solve(self, button: Button, interaction: discord.Interaction):

        await interaction.response.send_modal(SolveModal(self.captcha, self.role))

    @button(label="New captcha !", style=discord.ButtonStyle.red)
    async def new_captcha(self, button: Button, interaction: discord.Interaction):

        button.disabled = True

        await interaction.response.edit_message(view=self)

        self.captcha.new_captcha()

        await interaction.edit_original_response(
            embed=captchaEmbed(self.captcha),
            file=discord.File(self.captcha.captchaPath, "captcha.png"),
            view=self
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        return interaction.user == self.captcha.member
