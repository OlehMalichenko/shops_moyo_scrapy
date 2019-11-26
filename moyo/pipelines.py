from moyo.gclient import Gclient
from pprint import pprint



class MoyoPipeline(object):

    def __init__(self):
        self.client = Gclient()
        self.main_list = list()
        self.sheet = self.client.get_sheet()
        print('notice from pipeline init')

    def open_spider(self, spider):
        print('notice from pipeline: spider ' + spider.name + ' open')


    def close_spider(self, spider):
        print('notice from pipeline: spider ' + spider.name + ' close')
        self.write_sheet()


    def get_title(self):
        return [
            'name',
            'prod_id',
            'link',
            'price',
            'price_old',
            'available'
        ]


    def write_sheet(self):
        title = self.get_title()
        self.main_list.insert(0, title)

        last_row = len(self.main_list)
        last_col = len(title)

        cell_list = self.sheet.range(1, 1, last_row, last_col)

        for cell in cell_list:
            try:
                cell.value = self.main_list[cell.row - 1][cell.col - 1]
            except:
                cell.value = 'error read'

        self.sheet.update_cells(cell_list)





    def process_item(self, item, spider):
        block_list = list()
        block_list.append(item['name'])
        block_list.append(item['prod_id'])
        block_list.append(item['link'])
        block_list.append(item['price'])
        block_list.append(item['price_old'])
        block_list.append(item['available'])

        self.main_list.append(block_list)

        return item
