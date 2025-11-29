from java.io import File, IOException
from javax.imageio import ImageIO
from java.awt.image import BufferedImage 
from org.bukkit import Material, Location, Bukkit
import pyspigot as ps
# top left corner of canvas
canvasCorner = [-358, 300, 60]

currentTask = None
correspondingBlocks = {
    "white": Material.WHITE_CONCRETE,
    "light_gray": Material.LIGHT_GRAY_CONCRETE,
    "gray": Material.GRAY_CONCRETE,
    "black": Material.BLACK_CONCRETE,
    "brown": Material.BROWN_CONCRETE,
    "red": Material.RED_CONCRETE,
    "orange": Material.ORANGE_CONCRETE,
    "yellow": Material.YELLOW_CONCRETE,
    "lime": Material.LIME_CONCRETE,
    "green": Material.GREEN_CONCRETE,
    "cyan": Material.CYAN_CONCRETE,
    "light_blue": Material.LIGHT_BLUE_CONCRETE,
    "blue": Material.BLUE_CONCRETE,
    "purple": Material.PURPLE_CONCRETE,
    "magenta": Material.MAGENTA_CONCRETE,
    "pink": Material.PINK_CONCRETE,
    "beige": Material.OAK_PLANKS,
    "darker_beige": Material.SPRUCE_PLANKS,
    "light_beige": Material.BIRCH_PLANKS,
    "red2": Material.RED_TERRACOTTA,
    "pinkish": Material.POLISHED_GRANITE,
    "netherite_gray": Material.NETHERITE_BLOCK,
    "jungle_beige": Material.STRIPPED_JUNGLE_WOOD,
    "brick_red": Material.BRICKS,
    "mud_brown": Material.PACKED_MUD,
    "andesite_gray": Material.POLISHED_ANDESITE,
    "smooth_stone_gray": Material.SMOOTH_STONE,
    "crimson_hyphae_purple": Material.STRIPPED_CRIMSON_HYPHAE,
    "sandstone_beige": Material.SMOOTH_SANDSTONE,
    "green_wool": Material.GREEN_WOOL,
    "green_terracotta": Material.GREEN_TERRACOTTA,
    "packed_ice_blue": Material.PACKED_ICE,
    "red_nether_brick": Material.RED_NETHER_BRICKS,
    "lapis_blue": Material.LAPIS_BLOCK,
    "copper_green": Material.WAXED_OXIDIZED_COPPER,
    "blue_terracotta": Material.BLUE_TERRACOTTA,
    "light_gray_terracotta": Material.LIGHT_GRAY_TERRACOTTA,
    "white_terracotta": Material.WHITE_TERRACOTTA,
    "waxed_exposed_copper_brown": Material.WAXED_EXPOSED_COPPER,
    "copper_orange": Material.COPPER_BLOCK,
    "light_blue_terracotta": Material.LIGHT_BLUE_TERRACOTTA

}
correspondingColors = {
    "white": [231, 235, 235],
    "light_gray": [161, 163, 167],
    "gray": [54, 57, 61],
    "black": [8, 10, 15],
    "brown": [99, 62, 43],
    "red": [160, 39, 34],
    "orange": [224, 97, 0],
    "yellow": [240, 175, 21],
    "lime": [94, 168, 24],
    "green": [73, 91, 36],
    "cyan": [21, 119, 136],
    "light_blue": [35, 137, 198],
    "blue": [44, 46, 143],
    "purple": [121, 42, 172],
    "magenta": [149, 88, 108],
    "pink": [213, 101, 143],
    "beige": [189, 153, 98],
    "darker_beige": [129, 96, 58],
    "light_beige": [198, 181, 122],
    "red2": [142, 59, 45],
    "pinkish": [159, 107, 88],
    "netherite_gray": [77, 73, 77],
    "jungle_beige": [187, 141, 97],
    "brick_red": [157, 82, 65],
    "mud_brown": [118, 89, 64],
    "andesite_gray": [132, 135, 134],
    "smooth_stone_gray": [161, 161, 161],
    "crimson_hyphae_purple": [93, 26, 30],
    "sandstone_beige": [224, 214, 170],
    "green_wool": [85, 110, 27],
    "green_terracotta": [76, 83, 42],
    "packed_ice_blue": [141, 180, 250],
    "red_nether_brick": [70, 7, 9],
    "lapis_blue": [31, 67, 140],
    "copper_green": [83, 164, 134],
    "blue_terracotta": [74, 60, 91],
    "light_gray_terracotta": [135, 107, 98],
    "white_terracotta": [210, 178, 161],
    "waxed_exposed_copper_brown": [161, 126, 104],
    "copper_orange": [193, 108, 79],
    "light_blue_terracotta": [114, 109, 138]


}

class Image:
    def __init__(self, fileName):

        self.file = File(fileName)
        try:
            self.image = ImageIO.read(self.file)
        except Exception as e:
            return e
        self.width = self.image.width
        self.height = self.image.height
        self.currentX = 0 # keep these the same
        self.currentY = 0 # keep these the same
        self.currentIteration = 0 # keep these the same
        self.blocksPerTick = 90 # image is generated in chunks, this is how many blocks per chunk
    def euclideanDistance(self, rgb1, rgb2):

        r1 = rgb1[0]
        g1 = rgb1[1]
        b1 = rgb1[2]

        r2 = rgb2[0]
        g2 = rgb2[1]
        b2 = rgb2[2]

        euclideanDistance = (r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2 
        return euclideanDistance
    def getColorName(self, rgb):

        closestColor = None
        colorName = None
        minDistance = float("inf")
        for key, value in correspondingColors.items():
            distance = self.euclideanDistance(rgb, value)
            if distance < minDistance:
                minDistance = distance
                closestColor = value
                colorName = key

        return colorName


    def drawNextPartOfImage(self, world):
        global currentTask
        for i in range(self.blocksPerTick):
            if self.currentIteration >= self.width * self.height:
                ps.scheduler.stopTask(currentTask)
                currentTask = None
                return
            x = self.currentX
            y = self.currentY
            rgb = self.image.getRGB(x, y)
            red = (rgb >> 16) & 0xFF
            green = (rgb >> 8) & 0xFF
            blue = rgb & 0xFF

            color = self.getColorName(([int(red), int(green), int(blue)]))
            material = correspondingBlocks[color]
            if material:
                xToPlace = canvasCorner[0] - x
                yToPlace = canvasCorner[1] - y
                zToPlace = canvasCorner[2] #!! if I get around to it this will actually change so the picture can be different orientations
                
                locationToPlace = Location(world, xToPlace, yToPlace, zToPlace)
                block = world.getBlockAt(locationToPlace)

                block.setType(material)
                self.currentX += 1
                self.currentIteration += 1
                
            if self.currentX >= self.width:
                self.currentX = 0
                self.currentY += 1
def imageTask(pictureInstance):
    try:
        pictureInstance.drawNextPartOfImage(Bukkit.getServer().getWorlds()[0])
    except Exception as e:
        print(e)
        


def blockifyimage(sender, label, args):
    global currentTask
    if currentTask != None:
        sender.sendMessage("There's already a task running...try again after!")
        return True
    try:
        picture = Image(" ".join(args))
    except Exception as e:
        sender.sendMessage("An error occured! Did you write the correct file path + file name?")
        print(e)

    currentTask = ps.scheduler.scheduleRepeatingTask(imageTask, 0, 1, picture)

  
    return True
ps.command.registerCommand(blockifyimage, "blockifyimage")