from aip import AipImageClassify


def get_file_content(file_path):
    """
    读取图片
    :param file_path: 图片路径
    :return: 图片字节流
    """
    with open(file_path, 'rb') as fp:
        return fp.read()


class IR:

    def __init__(self, app_id, api_key, secret_key):
        self.client = AipImageClassify(app_id, api_key, secret_key)
        self.options = {}

    def do_image_recognition(self, image_file):
        image = get_file_content(image_file)
        contents = self.distinguish_general(image)
        type = contents.get("result")[0].get("root")
        keyword = contents.get("result")[0].get("keyword")
        if type in ["商品-食物"]:
            dishes = self.distinguish_dishes(image)
            print(dishes)
            message = "图片为食品："
            for dishe in dishes.get("result"):
                if message == "图片为食品：":
                    message += "\n"
                else:
                    message += "\n或者 "
                if dishe.get("has_calorie"):
                    calorie = dishe.get("calorie")
                else:
                    calorie = 0
                message += "名称：" + dishe.get("name") + "，每100克含有" + calorie + "千卡的卡路里"
            return message
        elif type in ["交通工具-汽车"]:
            cars = self.distinguish_cars(image)
            color = cars.get("color_result")
            if color is None:
                color = "无法识别"
            message = "图片中车体为" + color + "，可能为以下车型："
            for car in cars.get("result"):
                score = str(round(car.get("score") * 100))
                name = car.get("name")
                year = car.get("year")
                description = car.get("baike_info").get("description")
                if description is None:
                    description = "无描述"
                message += "\n" + name + "，出厂年份：" + year + "，（" + "可信度" + score + "%）\n" + description
            return message
        elif "动物" in type:
            animals = self.distinguish_animals(image)
            message = "图片为" + type + "，可能为以下品类："
            for animal in animals.get("result"):
                score = str(round(float(animal.get("score")) * 100))
                name = animal.get("name")
                description = animal.get("baike_info").get("description")
                if description is None:
                    description = "无描述"
                message += "\n" + name + "：（" + "可信度" + score + "%）\n" + description
            return message
        elif "植物" in type:
            plants = self.distinguish_plants(image)
            message = "图片为" + type + "，可能为以下品类："
            for plant in plants.get("result"):
                score = str(round(plant.get("score") * 100))
                name = plant.get("name")
                description = plant.get("baike_info").get("description")
                if description is None:
                    description = "无描述"
                message += "\n" + name + "：（" + "可信度" + score + "%）\n" + description
            return message
        else:
            message = "图片可能为以下内容："
            for content in contents.get("result"):
                print(content)
                keyword = str(content.get("keyword"))
                score = str(round(content.get("score") * 100))
                description = content.get("baike_info").get("description")
                if description is None:
                    description = "无描述"
                message += "\n" + keyword + "：（" + "可信度" + score + "%）\n" + description
            return message

    def distinguish_general(self, image):
        self.options["baike_num"] = 5
        results = self.client.advancedGeneral(image, self.options)
        print(results)
        return results

    def distinguish_dishes(self, image):
        """ 如果有可选参数 """
        self.options["top_num"] = 3
        self.options["filter_threshold"] = "0.7"
        self.options["baike_num"] = 5

        """ 带参数调用菜品识别 """
        results = self.client.dishDetect(image, self.options)
        print(results)
        return results

    def distinguish_cars(self, image):
        """ 如果有可选参数 """
        self.options["top_num"] = 3
        self.options["baike_num"] = 5

        """ 带参数调用车辆识别 """
        results = self.client.carDetect(image, self.options)
        print(results)
        return results

    def distinguish_logos(self, image):
        self.options["custom_lib"] = "true"

        """ 带参数调用logo商标识别 """
        results = self.client.logoSearch(image, self.options)
        print(results)
        return results

    def distinguish_animals(self, image):
        self.options["top_num"] = 3
        self.options["baike_num"] = 5

        """ 带参数调用动物识别 """
        results = self.client.animalDetect(image, self.options)
        print(results)
        return results

    def distinguish_plants(self, image):
        self.options["baike_num"] = 5

        """ 带参数调用植物识别 """
        results = self.client.plantDetect(image, self.options)
        print(results)
        return results


