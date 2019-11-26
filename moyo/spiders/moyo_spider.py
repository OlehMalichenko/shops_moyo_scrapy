import scrapy
from moyo.items import MoyoItem


class MoyoSpiderSpider(scrapy.Spider):
    name = 'moyo_spider'
    allowed_domains = ['moyo.ua']
    start_urls = ['https://www.moyo.ua/portal_brand/apple']


# ===========MAIN PARSE============== #
    def parse(self, response):
        try:
            blocks_1 = response.xpath('//div[@class="portal_pageblock clear_after"]')
        except:
            return
        else:
            for block1 in blocks_1:
                # start href for product
                href1 = self.get_href_1(block1)
                if href1 is not None:
                    yield response.follow(url=href1, callback=self.parse_block_products)
                    # break





# ============PAGE PARSE============= #
    def parse_block_products(self, response):
        block_products = response.xpath('//div[@id="goods-list"]//div[@class="product-tile_inner_hover_wrapper"]')

        for block_product in block_products:
            try:
                item = MoyoItem()

                # name
                item['name'] = block_product.xpath('.//figure/@data-alt').get()

                # product code
                item['prod_id'] = block_product.xpath('.//figure/@data-id').get()

                # product link
                item['link'] = response.urljoin(block_product.xpath('.//a[@class="gtm-link-product"]/@href').get())

                # price
                price_block = block_product.xpath('.//div[@class="product-tile_main-info"]')
                item['price'], item['price_old'], item['available'] = self.get_price_info(price_block)
            except:
                continue
            else:
                yield item

        # next url-pagination
        url_next = self.get_next_pagination(response)
        if url_next is not None:
            yield response.follow(url=url_next, callback=self.parse_block_products)





# ============HELP================= #
    def get_price_info(self, price_block):
        if price_block is None:
            return None, None, None
        else:

            price = None
            price_old = None
            available = 'No'

            try:
                price = price_block.xpath('.//div[@class="product-tile_price-current"]//span[@class="product-tile_price-value"]/text()').get()
                if price is not None:
                    available = 'Yes'
            except:
                return price, price_old, available

            else:
                try:
                    price_old = price_block.xpath('.//div[@class="product-tile_price-old"]//span[@class="product-tile_price-value"]/text()').get()
                finally:
                    return price, price_old, available

# !!! CHECK AVAILABLE !!!

    def get_next_pagination(self, response):
        """if block have pagination
            return next pagination url or None"""
        try:
            # get active-page
            pag_active = response.xpath('//div[@id="catalog-pagination"]//div[@class="new-pagination-pages-container"]/*[@class="new-pagination-link active"]')
            # get next href after active
            pag_next = pag_active.xpath('.//following-sibling::*/@href').get()
        except:
            return None
        else:
            if pag_next is not None:
                url_next = response.urljoin(pag_next)
                return url_next
            else:
                return None


    def get_href_1(self, block1):
        """return start hrefs for only product-block"""
        try:
            return block1.xpath('.//a[@class="foto_block vfixed-container"]/@href').get()
        except:
            return None
