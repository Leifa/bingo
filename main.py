#!/usr/bin/python2
import random
import sys
import cairosvg

BORDER = 50
CELL = 200
SIZE = 5*CELL + 2*BORDER

class Thumb:

    def make_thumbs(self, filename, color):
        filename = filename.replace("/", " ")
        f = open(filename, "r")
        counter = 1
        for line in f.readlines():
            line = line.replace("\\n", "\n")
            svg = self.make_thumb(line, color)
            thumbfilename = str(counter) + " " + line.replace("\n", " ")
            thumbfile = open(thumbfilename + ".svg", "w")
            thumbfile.write(svg)
            thumbfile.close()

            cairosvg.svg2png(url=thumbfilename + ".svg", write_to=thumbfilename + ".png")
            #os.remove(thumbfilename + ".svg")

            counter += 1

    def make_card_and_save(self, number, words):
        svg = self.make_card(words)
        thumbfilename = str(number)
        thumbfile = open(thumbfilename + ".svg", "w")
        thumbfile.write(svg)
        thumbfile.close()

        cairosvg.svg2png(url=thumbfilename + ".svg", write_to=thumbfilename + ".png")

    def make_card(self, words):
        svg = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        svg += f'<svg width="{SIZE}" height="{SIZE}">'
        svg += "<rect width=\"100%\" height=\"100%\" fill=\"white\" />"
        svg += self.makegrid()
        col = 0
        row = 0
        for word in words:
            x = BORDER + CELL/2 + col*CELL
            y = BORDER + CELL/2 + row*CELL
            col += 1
            if col == 5:
                col = 0
                row += 1
            svg += self.maketext(x, y, word)
        svg += "</svg>"
        return svg

    def maketext(self, x, y, text):
        svg = ""
        lines = []
        if len(text) <= 20:
            lines.append(text)
        else:
            while len(text) > 20:
                space = text.rfind(" ", 0, 20)
                lines.append(text[0:space])
                text = text[space:]
            lines.append(text)
        if len(lines) == 1:
            svg += self.makeline(x, y, lines[0], 20)
        elif len(lines) == 2:
            svg += self.makeline(x, y-15, lines[0], 20)
            svg += self.makeline(x, y+15, lines[1], 20)
        elif len(lines) == 3:
            svg += self.makeline(x, y-30, lines[0], 20)
            svg += self.makeline(x, y, lines[1], 20)
            svg += self.makeline(x, y+30, lines[2], 20)
        elif len(lines) == 4:
            svg += self.makeline(x, y - 45, lines[0], 20)
            svg += self.makeline(x, y - 15, lines[1], 20)
            svg += self.makeline(x, y + 15, lines[2], 20)
            svg += self.makeline(x, y + 30, lines[3], 20)
        return svg

    def makeline(self, x, y, line, fontsize):
        return "<text style=\"font-family:'Latin Modern Sans Demi Cond';fill:#" + "1e750c" + ";font-size:" + str(
            fontsize) + "px\" x=\"" + str(x) + "\" y=\"" + str(y) + "\" text-anchor=\"middle\">" + line + "</text>"

    def makegrid(self):
        svg = ""
        for i in range(6):
            x = BORDER + CELL*i
            svg += f'<line x1="{x}" y1="{BORDER}" x2="{x}" y2="{BORDER+5*CELL}" style="stroke:rgb(0,0,0);stroke-width:2"/>"'
        for i in range(6):
            y = BORDER + CELL*i
            svg += f'<line x1="{BORDER}" y1="{y}" x2="{BORDER+5*CELL}" y2="{y}" style="stroke:rgb(0,0,0);stroke-width:2"/>"'
        return svg

for i in range(10):
    all_words = open("words.txt").readlines()

    chosen_words = []

    for j in range(25):
        index = random.randint(0, len(all_words)-1)
        chosen_words.append(all_words[index].rstrip())
        del all_words[index]

    Thumb().make_card_and_save(i, chosen_words)