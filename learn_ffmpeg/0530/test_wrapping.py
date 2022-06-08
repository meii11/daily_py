from PIL import Image, ImageDraw, ImageFont


class ImgText:
    font = ImageFont.truetype("./data/simsun.ttc", 30)

    def __init__(self, text):
        # 预设宽度 可以修改成你需要的图片宽度
        self.width = 500
        # 文本
        self.text = text
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height = self.split_text()

    def get_duanluo(self, text):
        txt = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            width, height = draw.textsize(char, ImgText.font)
            sum_width += width
            if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count

    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height

    def draw_text(self):
        """
    绘图以及文字
    :return:
    """
        note_img = Image.open("./data/bg.jpg").convert("RGBA")
        draw = ImageDraw.Draw(note_img)
        # 左上角开始
        x, y = 300, 300
        for duanluo, line_count in self.duanluo:
            draw.text((x, y), duanluo, fill=(255, 0, 0), font=ImgText.font)
            y += self.line_height * line_count
        note_img.save("result.png")


if __name__ == '__main__':
    n = ImgText(
        "小编为a11，,.。大家讲解一下几位抗日名将的故事，第一位抗日\n名将杨靖宇，他不仅是白山黑水间的铁血将军，也是信念坚定的共产党员。他的威名，让敌人闻风丧胆，更令中国人骄傲。在1940"
        "年初，杨靖宇所带领的部队被日军围剿，他们已经断粮五天了，他和剩下的十几名战忍妥着饥饿，疲劳，与敌人奋战，后来其他战十都牺牲了，杨靖宇仍然边战边走。下面讲一讲狼牙山五壮士，1941年9月25"
        "日，数千名日asdasdasd伪军在河北易具狼牙山地区实施“清剿”。晋察冀一分区一团七连二排六班的5"
        "名战士，即班长马宝玉，副班长葛振林，战十胡德林、胡福才和宋学义，为掩护主力部队和群众转移，与敌人激烈战斗，利用有利地形奋勇还击，打日伪军多次进攻，毙伤90余人。第三个故事是刘胡兰的英雄事迹，1946年12"
        "月的一天，刘胡兰配合武工队员将“当地一害”石佩怀处死，阎锡山匪军恼羞成怒，决定实施报复行动。1947年1月12日，阎军突然袭击云周西村，刘胡兰因叛徒告密而被捕。刘胡兰烈士牺牲时，尚未满15"
        "周岁，是已知的中国共产党女烈十中年龄最小的一个。毛泽东在指挥全国战局之余，为刘胡兰题词:“生的伟大，死的光荣!")
    n.draw_text()